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

import shutil

import roundtrip_common

from literalizer.languages import Swift

_VAR_NAME = "myData"
_LABEL = "Swift"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Swift program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Swift(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
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
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.swift",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[swift, "-swift-version", "5", "main.swift"],
                failure_label="swift run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
