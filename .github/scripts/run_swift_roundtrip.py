"""Swift JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Swift
``let myData: Any = ...`` declaration, wrap it in a tiny ``main`` that
serializes ``myData`` back to JSON via ``JSONSerialization`` from
``Foundation`` and writes the bytes to stdout, run it with ``swift``,
and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-swift`` job in
``.github/workflows/lint.yml``, because that job is where the Swift
toolchain is installed.  It shares the same input and comparison logic
as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows ``Int64`` (the widest signed integer the
Swift backend's literal output supports), so the program would not
compile if the field were kept.  Same shape as the Go, TypeScript and
Zig exclusions.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Swift

_VAR_NAME = "myData"
_LABEL = "Swift"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Swift program literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Swift(),
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "import Foundation\n"
        f"{preamble}\n"
        f"{result.code}\n"
        "    let data = try JSONSerialization.data(\n"
        f"        withJSONObject: {_VAR_NAME},\n"
        "        options: [],\n"
        "    )\n"
        "    FileHandle.standardOutput.write(data)\n"
    )


def main() -> None:
    """Round-trip the shared document through the Swift backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    swift = shutil.which(cmd="swift") or "swift"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        (tmpdir / "main.swift").write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[swift, "-swift-version", "5", "main.swift"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: swift run error\n"
            f"{run_result.stdout}{run_result.stderr}",
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
