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
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import TypeScript

_VAR_NAME = "myData"
_LABEL = "TypeScript"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable TypeScript program literalized from
    *json_text*.
    """
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=TypeScript(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
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
    with tempfile.TemporaryDirectory() as tmpdir_name:
        script_path = Path(tmpdir_name) / "main.ts"
        script_path.write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[tsx, str(script_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: tsx runtime error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=_EXCLUDED_KEYS,
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
