"""PHP JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a PHP
``$myData = ...`` assignment, wrap it in a tiny script that prints
``json_encode($myData)``, run it with PHP, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Php roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the PHP toolchain is installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

Two fields are excluded from the comparison because PHP's JSON encoder
cannot represent them losslessly:

* ``biginteger`` -- the 26-digit literal overflows PHP's signed 64-bit
  integer and is widened to ``float``, so ``json_encode`` re-emits it
  as ``1.0e+26``.
* ``empty_object`` -- PHP has a single sequence/map array type, so an
  empty associative array is indistinguishable from an empty list and
  ``json_encode`` emits it as ``[]`` rather than ``{}``.
"""

import shutil

import roundtrip_common

from literalizer.languages import Php

_VAR_NAME = "myData"
_LABEL = "PHP"
_EXCLUDED_KEYS = ("biginteger", "empty_object")


def _build_program(json_text: str) -> str:
    """Return a runnable PHP program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Php(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\necho json_encode(${_VAR_NAME});\n"


def main() -> None:
    """Round-trip the shared document through the PHP backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    php = shutil.which(cmd="php") or "php"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.php",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[php, "main.php"],
                failure_label="php runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
