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
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Php

_VAR_NAME = "myData"
_LABEL = "PHP"


def _build_program(json_text: str) -> str:
    """Return a runnable PHP program literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Php(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\necho json_encode(${_VAR_NAME});\n"


def main() -> None:
    """Round-trip the shared document through the PHP backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    php = shutil.which(cmd="php") or "php"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        script_path = Path(tmpdir_name) / "main.php"
        script_path.write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[php, str(script_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: php runtime error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=("biginteger", "empty_object"),
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
