"""Ruby JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Ruby
``myData = ...`` assignment, wrap it in a tiny script that prints
``JSON.generate(myData)``, run it with Ruby, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Ruby roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the Ruby toolchain is installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Ruby

_VAR_NAME = "myData"
_LABEL = "Ruby"


def _build_program(json_text: str) -> str:
    """Return a runnable Ruby program literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Ruby(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "# frozen_string_literal: true\n"
        "\n"
        "require 'json'\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"STDOUT.write(JSON.generate({_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Ruby backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    ruby = shutil.which(cmd="ruby") or "ruby"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        script_path = Path(tmpdir_name) / "main.rb"
        script_path.write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[ruby, str(script_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: ruby runtime error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        sys.exit(1)
    roundtrip_common.verify(label=_LABEL, produced_json=run_result.stdout)
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
