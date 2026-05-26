"""Zig JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Zig
``const myData = ...`` declaration under
``json_type=Zig.JsonTypes.STD_JSON_VALUE`` (so the binding is a
``std.json.Value`` tree), wrap it in a tiny ``main`` that hands
``myData`` straight to ``std.json.stringify`` on stdout, run it with
``zig run``, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-zig`` job in
``.github/workflows/lint.yml``, because that job is where the Zig
toolchain is installed.  It shares the same input and comparison logic
as the other per-language round-trip helpers.

``std.json.Value`` carries integers wider than ``i64`` as ``.number_string``
which ``std.json.stringify`` writes back verbatim, so the shared input's
26-digit ``biginteger`` field needs no exclusion under this strategy.
"""

import shutil

import roundtrip_common

from literalizer.languages import Zig

_VAR_NAME = "myData"
_LABEL = "Zig"


def _build_program(json_text: str) -> str:
    """Return a runnable Zig program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Zig(json_type=Zig.json_types.STD_JSON_VALUE),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    preamble = "\n".join(result.preamble)
    # The ``STD_JSON_VALUE`` declaration references ``allocator``;
    # ``wrap_in_file=False`` so the helper does not emit the arena setup
    # itself, and this round-trip needs its own ``main`` anyway to call
    # ``std.json.stringify``.
    return (
        f"{preamble}\n"
        "pub fn main() !void {\n"
        "    var arena = std.heap.ArenaAllocator.init(\n"
        "        std.heap.page_allocator,\n"
        "    );\n"
        "    defer arena.deinit();\n"
        "    const allocator = arena.allocator();\n"
        f"{result.code}\n"
        "    const stdout = std.io.getStdOut().writer();\n"
        f"    try std.json.stringify({_VAR_NAME}, .{{}}, stdout);\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Zig backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    zig = shutil.which(cmd="zig") or "zig"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.zig",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[zig, "run", "main.zig"],
                failure_label="zig run error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
