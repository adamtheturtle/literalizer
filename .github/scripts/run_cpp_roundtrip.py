"""C++ JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a C++
``auto my_data = nlohmann::json::parse(...);`` declaration via
``Cpp(json_type=NLOHMANN_JSON)``, wrap it in a tiny ``main`` that writes
``my_data.dump()`` to stdout, compile and run it with ``clang++``, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-cpp`` job in
``.github/workflows/lint.yml``, because that job is where the C++
toolchain (``clang++``) and the ``nlohmann-json3-dev`` package are
already installed.  It shares the same input and comparison logic as
the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the
comparison: its 26-digit value overflows ``nlohmann::json``'s
``int64_t`` integer node, same shape as the Go, TypeScript, Zig, Swift,
Rust and D exclusions.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Cpp

_VAR_NAME = "my_data"
_LABEL = "C++"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable C++ program literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "#include <iostream>\n"
        "int main() {\n"
        f"{result.code}\n"
        f"    std::cout << {_VAR_NAME}.dump();\n"
        "    return 0;\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the C++ backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    clangxx = shutil.which(cmd="clang++") or "clang++"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        src = tmpdir / "main.cpp"
        src.write_text(data=program, encoding="utf-8")
        binary = tmpdir / "main"
        compile_result = subprocess.run(
            args=[
                clangxx,
                "-std=c++20",
                str(object=src),
                "-o",
                str(object=binary),
            ],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
        if compile_result.returncode != 0:
            sys.stderr.write(
                f"{_LABEL}: clang++ error\n"
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
