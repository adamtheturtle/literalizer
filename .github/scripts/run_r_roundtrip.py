"""R JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an R
``my_data <- ...`` assignment, wrap it in a tiny script that prints
``jsonlite::toJSON(my_data, auto_unbox = TRUE)``, run it with
``Rscript``, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``R roundtrip`` step of the ``lint-r``
job in ``.github/workflows/lint.yml``, because that job is where the R
toolchain is installed and the ``jsonlite`` package is provisioned
(``R_LIBS_USER`` points the script's ``Rscript`` subprocess at that
package directory so ``library(jsonlite)`` resolves).  It shares the
same input and comparison logic as the other per-language round-trip
helpers.

Three top-level keys are excluded from the comparison:

* ``biginteger`` — its 26-digit value overflows R's double-precision
  numeric, same shape as the Go, TypeScript, Zig, Swift, Rust, D, and
  C++ exclusions.
* ``float_large_exponent`` — R's parser rounds the literal
  ``1.7976931348623157e+308`` up to ``Inf``, which ``jsonlite`` then
  serializes as the JSON string ``"Inf"`` rather than a number.
* ``empty_object`` — R represents both arrays and objects as ``list()``
  and an empty unnamed ``list()`` is genuinely ambiguous, so
  ``jsonlite`` serializes the empty-object value as ``[]`` instead of
  ``{}``.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import R

_VAR_NAME = "my_data"
_LABEL = "R"
_EXCLUDED_KEYS = ("biginteger", "float_large_exponent", "empty_object")


def _build_program(json_text: str) -> str:
    """Return a runnable R program literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=R(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "library(jsonlite)\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"cat(jsonlite::toJSON({_VAR_NAME}, auto_unbox = TRUE, "
        'digits = NA, null = "null"))\n'
    )


def main() -> None:
    """Round-trip the shared document through the R backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    rscript = shutil.which(cmd="Rscript") or "Rscript"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        script_path = Path(tmpdir_name) / "main.R"
        script_path.write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[rscript, "--no-init-file", str(script_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            env={**os.environ},
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: Rscript runtime error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        sys.stderr.write(f"\nProgram:\n{program}\n")
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=_EXCLUDED_KEYS,
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
