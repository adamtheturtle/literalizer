"""Crystal JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Crystal
``my_data = JSON.parse(%(...))`` assignment via
``Crystal(json_type=JSON_ANY)``, append a ``print my_data.to_json``
statement, compile and run the resulting program with ``crystal run``,
and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-crystal`` job in
``.github/workflows/lint.yml``, because that job is where the Crystal
toolchain is already installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the
comparison: its 26-digit value overflows the ``Int64`` integer node
that Crystal's ``JSON.parse`` exposes, same shape as the Go,
TypeScript, Zig, Swift, Rust, D and C++ exclusions.  The
``string_escapes`` field is excluded because the
``Crystal(json_type=JSON_ANY)`` backend rejects literal backslashes and
double quotes inside string values: they would be reinterpreted by the
``%(...)`` percent literal before the JSON parser sees them.
"""

import shutil

import roundtrip_common

from literalizer.languages import Crystal

_VAR_NAME = "my_data"
_LABEL = "Crystal"
_EXCLUDED_KEYS = ("biginteger", "string_escapes")


def _build_program(json_text: str) -> str:
    """Return a runnable Crystal program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Crystal(json_type=Crystal.json_types.JSON_ANY),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\nprint {_VAR_NAME}.to_json\n"


def main() -> None:
    """Round-trip the shared document through the Crystal backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    crystal = shutil.which(cmd="crystal") or "crystal"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.cr",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[crystal, "run", "main.cr"],
                failure_label="crystal run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
