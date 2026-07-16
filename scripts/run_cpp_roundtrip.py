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

The shared input's ``biginteger`` field is trimmed before
literalization: its 26-digit value overflows the unsigned 64-bit range
(the widest C++ literal the literalizer emits, via a ``ULL`` suffix),
so the literalizer raises
:class:`literalizer.exceptions.UnrepresentableIntegerError` rather than
emit code ``clang++`` would reject.  Same shape as the Go, TypeScript,
Zig, Swift, Rust and D exclusions.
"""

import shutil

from literalizer.languages import Cpp
from scripts import roundtrip_common

_VAR_NAME = "my_data"
_LABEL = "C++"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable C++ program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
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
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.cpp",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[clangxx, "-std=c++20", "main.cpp", "-o", "main"],
                failure_label="clang++ error",
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
