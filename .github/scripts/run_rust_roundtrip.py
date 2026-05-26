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
serialization.  Values above the ``i128`` range have no native Rust
literal and raise
:class:`literalizer.exceptions.UnrepresentableIntegerError` at
literalize time.  Same shape as the Go, TypeScript, and Zig exclusions.
"""

import shutil
import sys

import roundtrip_common

from literalizer.languages import Rust

_VAR_NAME = "my_data"
_LABEL = "Rust"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Rust program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Rust(json_type=Rust.json_types.SERDE_JSON_VALUE),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
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
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.rs",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    rustc,
                    "--edition",
                    "2021",
                    "-L",
                    f"dependency={deps_dir}",
                    "--extern",
                    f"serde_json={serde_json_rlib}",
                    "main.rs",
                    "-o",
                    "main",
                ],
                failure_label="rustc error",
            ),
            roundtrip_common.Step(
                args=["./main"],
                failure_label="run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
