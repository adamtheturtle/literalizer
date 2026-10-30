"""JavaScript JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a JavaScript
``const myData = ...;`` declaration, wrap it in a tiny script that
writes ``JSON.stringify(myData)`` to stdout, run it with ``node``, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-fast`` job in
``.github/workflows/lint.yml``, because that job is where the Node
toolchain is already installed for the ``Lint JavaScript`` step.  It
follows the same template as ``run_typescript_roundtrip.py``: a single
``.py`` file, no separate serializer source, because ``JSON.stringify``
is in the JavaScript standard library.

The shared input's ``biginteger`` field is excluded before literalization:
JavaScript cannot represent it as a safe ``Number`` and the backend rejects
it rather than emitting a lossy numeric literal.
"""

import datetime as dt
import json
import shutil

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import JavaScript
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "JavaScript"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable JavaScript program literalized from
    *json_text*.
    """
    result = roundtrip_common.literalize_new_variable(
        language=JavaScript(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        f"{result.code}\n"
        f'if (!Object.is({_VAR_NAME}["negative_zero"], -0)) {{\n'
        '  throw new Error("negative_zero lost its sign");\n'
        "}\n"
        f"process.stdout.write(JSON.stringify({_VAR_NAME}));\n"
    )


def _check_native_datetime_offsets(*, node: str) -> None:
    """Check exact instants with offsets outside ISO parser syntax."""
    cases = (
        (1970, 0, 1_000_000, -1000),
        (1970, 0, -1_000_000, 1000),
        (1970, 1, 1, 0),
        (1970, 1000, 1000, 0),
        (1970, 999999, -1, 1000),
        (1970, 123456, 123456, 0),
        (1970, 123456, 122456, 1),
        (1, 0, 1_000_000, -62_135_596_801_000),
    )
    stamps = [
        dt.datetime(
            year=year,
            month=1,
            day=1,
            microsecond=wall,
            tzinfo=dt.timezone(offset=dt.timedelta(microseconds=offset)),
        )
        for year, wall, offset, _milliseconds in cases
    ]
    result = literalize(
        source='{"$ref": "stamps"}',
        input_format=InputFormat.JSON,
        language=JavaScript(),
        variable_form=NewVariable(name=_VAR_NAME, modifiers=frozenset()),
        ref_key="$ref",
        bound_refs={"stamps": stamps},
        wrap_in_file=True,
    )
    program = (
        f"{result.code}\n"
        f"const milliseconds = {_VAR_NAME}.map(value => {{\n"
        '  if (!(value instanceof Date)) throw new Error("expected Date");\n'
        "  return value.getTime();\n"
        "});\n"
        "process.stdout.write(JSON.stringify({milliseconds}));\n"
    )
    roundtrip_common.execute(
        label="JavaScript native datetime offsets",
        source_filename="offsets.js",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[node, "offsets.js"],
                failure_label="JavaScript datetime instant mismatch",
            ),
        ],
        excluded_keys=(),
        expected_json=json.dumps(
            obj={"milliseconds": [row[3] for row in cases]}
        ),
        extra_files=None,
    )


def main() -> None:
    """Round-trip the shared document through the JavaScript backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=JavaScript.variant_metadata.round_trip_capabilities,
    )
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    program = _build_program(json_text=trimmed_json)
    node = shutil.which(cmd="node")
    if node is None or node == "":
        node = "node"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.js",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[node, "main.js"],
                failure_label="node runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        expected_json=json_text,
        extra_files=None,
    )
    _check_native_datetime_offsets(node=node)


if __name__ == "__main__":
    main()
