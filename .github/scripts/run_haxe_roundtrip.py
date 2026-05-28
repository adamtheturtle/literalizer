"""Haxe JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Haxe
``final myData = ([...] : Map<String, Dynamic>)`` binding, wrap it in a
tiny ``class Main`` whose ``main()`` prints ``haxe.Json.stringify(myData)``
from the Haxe standard library, run it under ``haxe --interp``, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-haxe`` job in
``.github/workflows/lint.yml``, because that job is where the Haxe
toolchain is already installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the
comparison: the literalized program represents the 26-digit value as
an ``Int`` literal, which the eval/``--interp`` target promotes to
``Float`` (losing precision well before the round-trip back to JSON).
Trimming the field before literalization keeps the generated program
free of values the eval target would silently coerce.
"""

import shutil

import roundtrip_common

from literalizer.languages import Haxe

_VAR_NAME = "myData"
_LABEL = "Haxe"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Haxe program literalized from *json_text*."""
    trimmed = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Haxe(),
        json_text=trimmed,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "class Main {\n"
        "  static function main() {\n"
        f"    {result.code}\n"
        f"    Sys.print(haxe.Json.stringify({_VAR_NAME}));\n"
        "  }\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Haxe backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    haxe = shutil.which(cmd="haxe") or "haxe"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="Main.hx",
        program=program,
        steps=(
            roundtrip_common.Step(
                args=(haxe, "--main", "Main", "--interp"),
                failure_label="haxe --interp error",
            ),
        ),
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
