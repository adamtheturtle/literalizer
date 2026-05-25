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

The shared input's ``biginteger`` field is excluded from the comparison:
the literalizer emits a plain numeric literal, which JavaScript stores
as an IEEE-754 double, so the original 26-digit integer cannot survive
the round-trip even with a custom serializer.
"""

import shutil

import roundtrip_common

from literalizer.languages import JavaScript

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
        f"process.stdout.write(JSON.stringify({_VAR_NAME}));\n"
    )


def main() -> None:
    """Round-trip the shared document through the JavaScript backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    node = shutil.which(cmd="node") or "node"
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
    )


if __name__ == "__main__":
    main()
