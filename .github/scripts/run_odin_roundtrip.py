"""Odin JSON round-trip check (issue #2670).

Literalize the shared ``roundtrip_input.json`` document to an Odin
``my_data := _json_parse(`...`)`` binding under
``Odin(json_type=Odin.json_types.JSON_VALUE)``, wrap it in a tiny
``main`` that hands the resulting ``json.Value`` to ``json.marshal``
(which dispatches on the active variant of the
``core:encoding/json`` sum type), print the emitted JSON, run it with
``odin run .``, and hand the output to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-odin`` job in
``.github/workflows/lint.yml``, because that job is where the Odin
toolchain is installed.  It shares the same input and comparison logic
as the other per-language round-trip helpers, mirroring the Crystal /
Haskell / Zig / C++ / OCaml / PureScript scripts.

The shared input's ``biginteger`` field is excluded from the
comparison: its 26-digit value overflows ``Integer`` (i64) inside the
``json.Value`` sum type, so ``json.parse_string`` would reject it.
Same shape as the Go, TypeScript, V, Zig, Swift, Rust, D, C++ and
Crystal exclusions.
"""

import shutil

import roundtrip_common

from literalizer.languages import Odin

_VAR_NAME = "my_data"
_LABEL = "Odin"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Odin program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Odin(json_type=Odin.json_types.JSON_VALUE),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    preamble = "\n".join(result.preamble)
    return (
        f"{preamble}\n"
        'import "core:fmt"\n'
        "\n"
        "main :: proc() {\n"
        f"{result.code}\n"
        f"\tbytes, _ := json.marshal({_VAR_NAME})\n"
        "\tfmt.print(string(bytes))\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Odin backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    odin = shutil.which(cmd="odin") or "odin"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.odin",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[odin, "run", ".", "-out:prog"],
                failure_label="odin run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
