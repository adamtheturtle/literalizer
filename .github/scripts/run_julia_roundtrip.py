"""Julia JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Julia
``my_data = ...`` assignment, wrap it in a tiny script that prints
``JSON.json(my_data)``, run it with Julia, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Julia roundtrip`` step of the
``lint-julia`` job in ``.github/workflows/lint.yml``, because that job
is where the Julia toolchain is installed and a project with the
``JSON`` package is provisioned (the ``JULIA_PROJECT`` env var is set
there so ``using JSON`` resolves).  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows Julia's ``Int64`` so the literal is parsed
as ``Int128`` / ``BigInt`` and ``JSON.json`` for big integers cannot be
relied on across versions to emit a JSON-number representation matching
the input.  Same shape as the Go, TypeScript, Zig, Rust, and Elm
exclusions.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Julia

_VAR_NAME = "my_data"
_LABEL = "Julia"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Julia program literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Julia(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "using JSON\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"print(JSON.json({_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Julia backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    julia = shutil.which(cmd="julia") or "julia"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        script_path = Path(tmpdir_name) / "main.jl"
        script_path.write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[julia, "--startup-file=no", str(script_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            env={**os.environ},
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: julia runtime error\n{run_result.stdout}"
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
