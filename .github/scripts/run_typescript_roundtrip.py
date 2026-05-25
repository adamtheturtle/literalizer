"""TypeScript JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a TypeScript
``const myData = ...;`` declaration, wrap it in a tiny script that
writes ``JSON.stringify(myData)`` to stdout, run it with ``tsx``, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-typescript-run`` job in
``.github/workflows/lint.yml``, because that job is where the Node and
``tsx`` toolchain are installed.  It follows the same template as
``run_ruby_roundtrip.py``: a single ``.py`` file, no separate serializer
source, because ``JSON.stringify`` is in the JavaScript standard
library.

The shared input's ``biginteger`` field is excluded from the comparison:
the literalizer emits a plain numeric literal, which JavaScript stores
as an IEEE-754 double, so the original 26-digit integer cannot survive
the round-trip even with a custom serializer.
"""

import shutil

import roundtrip_common

from literalizer.languages import TypeScript

_VAR_NAME = "myData"
_LABEL = "TypeScript"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable TypeScript program literalized from
    *json_text*.
    """
    result = roundtrip_common.literalize_new_variable(
        language=TypeScript(),
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
    """Round-trip the shared document through the TypeScript backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    tsx = shutil.which(cmd="tsx") or "tsx"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.ts",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[tsx, "main.ts"],
                failure_label="tsx runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
