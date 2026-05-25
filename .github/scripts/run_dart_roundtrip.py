"""Dart JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Dart
``final my_data = <String, dynamic>{...}`` assignment, wrap it in a
tiny program that prints ``jsonEncode(my_data)`` from ``dart:convert``,
run it with ``dart run``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-dart`` job in
``.github/workflows/lint.yml``, because that job is where the Dart
toolchain is already installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the
comparison: the literalized program represents the 26-digit value as
a ``BigInt`` instance, which ``dart:convert``'s ``jsonEncode`` does
not know how to serialize.  Trimming the field before literalization
keeps the generated program free of values the standard JSON encoder
would reject.
"""

import shutil

import roundtrip_common

from literalizer.languages import Dart

_VAR_NAME = "my_data"
_LABEL = "Dart"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Dart program literalized from *json_text*."""
    trimmed = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Dart(),
        json_text=trimmed,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "import 'dart:convert';\n"
        f"{preamble}\n"
        "void main() {\n"
        f"  {result.code}\n"
        f"  print(jsonEncode({_VAR_NAME}));\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Dart backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    dart = shutil.which(cmd="dart") or "dart"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.dart",
        program=program,
        steps=(
            roundtrip_common.Step(
                args=(dart, "run", "main.dart"),
                failure_label="dart run error",
            ),
        ),
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
