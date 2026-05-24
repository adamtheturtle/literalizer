"""D JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a D
``auto my_data = JSONValue(...);`` declaration via the default
``std.json.JSONValue`` model, wrap it in a tiny ``void main`` that
serializes ``my_data`` back to JSON via ``JSONValue.toString`` and writes
it to stdout, compile and run it with ``dmd``, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-d`` job in
``.github/workflows/lint.yml``, because that job is where the D
toolchain (``dmd``) is already installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows D's 64-bit ``long`` (the widest integer the
``JSONValue`` integer node can carry), so the program would not compile
if the field were kept.  Same shape as the Go, TypeScript, Zig, Swift
and Rust exclusions.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import D

_VAR_NAME = "my_data"
_LABEL = "D"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable D program literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=D(),
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "import std.stdio;\n"
        "void main() {\n"
        f"{result.code}\n"
        f"    write({_VAR_NAME}.toString());\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the D backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    dmd = shutil.which(cmd="dmd") or "dmd"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        src = tmpdir / "main.d"
        src.write_text(data=program, encoding="utf-8")
        binary = tmpdir / "main"
        compile_result = subprocess.run(
            args=[
                dmd,
                f"-of={binary}",
                f"-od={tmpdir}",
                str(object=src),
            ],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
        if compile_result.returncode != 0:
            sys.stderr.write(
                f"{_LABEL}: dmd error\n"
                f"{compile_result.stdout}{compile_result.stderr}",
            )
            sys.stderr.write(f"\nProgram:\n{program}\n")
            sys.exit(1)
        run_result = subprocess.run(
            args=[str(object=binary)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: run error\n{run_result.stdout}{run_result.stderr}",
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
