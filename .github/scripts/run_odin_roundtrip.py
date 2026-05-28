"""Odin JSON round-trip check (issue #2670).

Literalize the shared ``roundtrip_input.json`` document to an Odin
``my_data := map[string]any{ ... }`` binding (default ``ERROR``
heterogeneous strategy, where the top-level dict's mixed scalar +
container values are kept inside a single ``map[string]any``), wrap it
in a tiny ``main`` that walks the ``any`` tree to JSON via a small
recursive emitter and prints the result, run it with ``odin run .``,
and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-odin`` job in
``.github/workflows/lint.yml``, because that job is where the Odin
toolchain is installed.  It shares the same input and comparison logic
as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the
comparison: its 26-digit value overflows the ``int`` (i64) default
Odin assigns to an integer literal stored as ``any``, so the program
would not compile if the field were kept.  Same shape as the Go,
TypeScript, V, Zig, Swift, Rust, D, C++ and Crystal exclusions.

Odin's standard ``core:encoding/json`` ``marshal`` explicitly rejects
``[dynamic]any`` and ``map[string]any`` -- the two container types
this literalized document is built from.  The ``Type_Info_Any`` arm of
``core/encoding/json/marshal.odin`` (``marshal.odin:251`` in
``dev-2026-04``) returns ``.Unsupported_Type``, and both the
dynamic-array and map arms (``marshal.odin:313`` and ``:343``) recurse
with each element typed as the *static* ``info.elem.id`` -- which is
``any`` itself for these containers, falling straight into the
rejecting arm.  ``json.marshal(map[string]int{...})`` works, but
``json.marshal(map[string]any{...})`` cannot.

So the emitter is hand-rolled: a ``type switch`` dispatches each
``any`` to one of the literal types the document can carry (``int``,
``f64``, ``bool``, ``string``, ``[dynamic]any``, ``map[string]any``)
and delegates the scalar leaves to ``json.marshal`` so string
escaping, float formatting, and ``-0.0`` are still the standard
library's problem rather than ours.

This is temporary: issue #2751 tracks adding
``Odin(json_type=JSON_VALUE)`` so the document is literalized as a
``json.Value`` tree, which ``json.marshal`` *does* unwrap correctly
(via the ``Type_Info_Union`` arm at ``marshal.odin:534``).  Once that
lands this helper drops the walker and calls ``json.marshal`` on the
literalized value directly, mirroring the Crystal / Haskell / Zig /
C++ round-trip scripts.
"""

import shutil

import roundtrip_common

from literalizer.languages import Odin

_VAR_NAME = "my_data"
_LABEL = "Odin"
_EXCLUDED_KEYS = ("biginteger",)

# Hand-rolled JSON emitter for the ``any``-typed value tree the
# literalized document produces.  Each arm of the type switch matches
# exactly one of the concrete types the literal can carry; scalar
# arms call ``json.marshal`` so escaping/formatting stays standard.
_EMIT = """
emit :: proc(b: ^strings.Builder, v: any) {
\tswitch x in v {
\tcase int:
\t\tbytes, _ := json.marshal(x)
\t\tstrings.write_bytes(b, bytes)
\tcase f64:
\t\tbytes, _ := json.marshal(x)
\t\tstrings.write_bytes(b, bytes)
\tcase bool:
\t\tbytes, _ := json.marshal(x)
\t\tstrings.write_bytes(b, bytes)
\tcase string:
\t\tbytes, _ := json.marshal(x)
\t\tstrings.write_bytes(b, bytes)
\tcase [dynamic]any:
\t\tstrings.write_byte(b, '[')
\t\tfor elem, i in x {
\t\t\tif i > 0 { strings.write_byte(b, ',') }
\t\t\temit(b, elem)
\t\t}
\t\tstrings.write_byte(b, ']')
\tcase map[string]any:
\t\tstrings.write_byte(b, '{')
\t\ti := 0
\t\tfor k, val in x {
\t\t\tif i > 0 { strings.write_byte(b, ',') }
\t\t\tkbytes, _ := json.marshal(k)
\t\t\tstrings.write_bytes(b, kbytes)
\t\t\tstrings.write_byte(b, ':')
\t\t\temit(b, val)
\t\t\ti += 1
\t\t}
\t\tstrings.write_byte(b, '}')
\t}
}
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Odin program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Odin(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    preamble = "\n".join(result.preamble)
    return (
        f"{preamble}\n"
        'import "core:encoding/json"\n'
        'import "core:fmt"\n'
        'import "core:strings"\n'
        f"{_EMIT}"
        "\n"
        "main :: proc() {\n"
        f"{result.code}\n"
        "\tb: strings.Builder\n"
        "\tstrings.builder_init(&b)\n"
        f"\temit(&b, {_VAR_NAME})\n"
        "\tfmt.print(strings.to_string(b))\n"
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
