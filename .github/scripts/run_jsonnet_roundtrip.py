"""Jsonnet JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Jsonnet
expression, write it to a ``.jsonnet`` file, and evaluate it with the
``jsonnet`` interpreter.  Jsonnet is a JSON superset whose evaluator
emits JSON on stdout, so there is no separate "back to JSON" step: the
interpreter is both the language runtime and the serializer.  The
emitted JSON is then handed to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-go-installed`` job in
``.github/workflows/lint.yml``, because that job is where the
``jsonnet`` binary (installed via ``go install
github.com/google/go-jsonnet/cmd/jsonnet``) is already on the PATH.
It shares the same input and comparison logic as the other
per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison
because Jsonnet numbers are IEEE 754 doubles, so the 26-digit literal
rounds when the evaluator emits it.  Same shape as the Go, TypeScript,
Zig, Rust, and Elm exclusions.

Jsonnet has no concept of a top-level named binding
(``supports_variable_names`` is ``False``), so the literalized output
is a bare expression rather than a ``local myData = ...;`` declaration.
The whole file evaluates to that expression, which is exactly what we
want.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, literalize
from literalizer.languages import Jsonnet

_LABEL = "Jsonnet"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a Jsonnet program literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Jsonnet(),
        pre_indent_level=0,
        include_delimiters=True,
        wrap_in_file=False,
    )
    return f"{result.code}\n"


def main() -> None:
    """Round-trip the shared document through the Jsonnet backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    jsonnet = shutil.which(cmd="jsonnet") or "jsonnet"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        program_path = tmpdir / "main.jsonnet"
        program_path.write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[jsonnet, str(program_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: jsonnet error\n{run_result.stdout}{run_result.stderr}",
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
