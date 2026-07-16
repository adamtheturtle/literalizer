"""Objective-C JSON round-trip check (issue #2668).

Literalize the shared ``roundtrip_input.json`` document to an
Objective-C ``id myData = @{...};`` declaration, wrap it in a tiny
``main`` that serializes ``myData`` back to JSON via
``NSJSONSerialization`` from ``Foundation`` and writes the bytes to
stdout, compile and run it with ``clang``, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-objectivec`` job in
``.github/workflows/lint.yml``, because that job is where the
Objective-C toolchain (Apple ``clang`` plus the ``Foundation``
framework) is already available.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the
comparison: its 26-digit value overflows the widest integer literal
the Objective-C backend emits (``unsigned long long``), so the
program would not compile if the field were kept.  Same shape as the
C++, Go, TypeScript, Zig, Swift, Rust and D exclusions.
"""

import shutil

from literalizer.languages import ObjectiveC
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Objective-C"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Objective-C program literalized from
    *json_text*.
    """
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=ObjectiveC(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "int main(void) {\n"
        "@autoreleasepool {\n"
        f"{result.code}\n"
        "    NSData *jsonData = [NSJSONSerialization\n"
        f"        dataWithJSONObject:{_VAR_NAME}\n"
        "        options:0\n"
        "        error:nil];\n"
        "    NSFileHandle *out =\n"
        "        [NSFileHandle fileHandleWithStandardOutput];\n"
        "    [out writeData:jsonData];\n"
        "}\n"
        "    return 0;\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Objective-C backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    clang = shutil.which(cmd="clang") or "clang"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.m",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    clang,
                    "-framework",
                    "Foundation",
                    "-Werror",
                    "main.m",
                    "-o",
                    "main",
                ],
                failure_label="clang error",
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
