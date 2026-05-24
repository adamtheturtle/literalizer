"""Rust JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Rust
``let my_data: serde_json::Value = ...`` declaration via the
``json_type=SERDE_JSON_VALUE`` strategy, wrap it in a tiny ``main`` that
prints ``serde_json::to_string(&my_data)``, compile and run it with
``rustc`` linked against ``serde_json``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-rust`` job in
``.github/workflows/lint.yml``, because that job is where the Rust
toolchain and a prebuilt ``libserde_json-*.rlib`` are already available.
It shares the same input and comparison logic as the other per-language
round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value fits in ``i128`` (which the Rust backend emits) but
``serde_json::Value`` stores numbers as ``i64``/``u64``/``f64``, so the
``json!`` macro would coerce it to a ``f64`` and lose precision before
serialization. Same shape as the Go, TypeScript, and Zig exclusions.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Rust

_VAR_NAME = "my_data"
_LABEL = "Rust"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Rust program literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Rust(json_type=Rust.json_types.SERDE_JSON_VALUE),
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "fn main() {\n"
        f"{result.code}\n"
        f"    let out = serde_json::to_string(&{_VAR_NAME}).unwrap();\n"
        '    print!("{}", out);\n'
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Rust backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    rustc = shutil.which(cmd="rustc") or "rustc"
    deps_dir = sys.argv[1]
    serde_json_rlib = sys.argv[2]
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        src = tmpdir / "main.rs"
        src.write_text(data=program, encoding="utf-8")
        binary = tmpdir / "main"
        compile_result = subprocess.run(
            args=[
                rustc,
                "--edition",
                "2021",
                "-L",
                f"dependency={deps_dir}",
                "--extern",
                f"serde_json={serde_json_rlib}",
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
                f"{_LABEL}: rustc error\n"
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
