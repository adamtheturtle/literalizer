"""Zig JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Zig
``const myData: ZVal = ...`` declaration, wrap it in a tiny ``main``
that converts ``myData`` into a ``std.json.Value`` tree and serializes
it back to JSON via ``std.json.stringify``, run it with ``zig run``,
and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-zig`` job in
``.github/workflows/lint.yml``, because that job is where the Zig
toolchain is installed.  It shares the same input and comparison logic
as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows ``u64`` (the widest unsigned integer the
Zig backend's generated ``ZVal`` union carries), so the program would
not compile if the field were kept.  Same shape as the Go and
TypeScript exclusions.
"""

import shutil

import roundtrip_common

from literalizer.languages import Zig

_VAR_NAME = "myData"
_LABEL = "Zig"
_EXCLUDED_KEYS = ("biginteger",)

# Build a ``std.json.Value`` tree mirroring ``ZVal`` and let
# ``std.json.stringify`` do the emission. ``.arr`` and ``.set`` share
# the ``[]const ZVal`` payload type, so one switch prong handles both;
# ``.nil`` and ``.uint`` never appear in the shared input (it is
# ``null``-free and ``biginteger`` is excluded) but the union is
# exhaustive so the prongs are still required.
_TO_JSON_VALUE = r"""
fn toJsonValue(allocator: std.mem.Allocator, v: ZVal) !std.json.Value {
    return switch (v) {
        .nil => .{ .null = {} },
        .bool => |b| .{ .bool = b },
        .int => |i| .{ .integer = i },
        .uint => |u| .{ .integer = @intCast(u) },
        .float => |f| .{ .float = f },
        .str => |s| .{ .string = s },
        .arr, .set => |a| blk: {
            var arr = std.json.Array.init(allocator);
            for (a) |item| try arr.append(try toJsonValue(allocator, item));
            break :blk .{ .array = arr };
        },
        .map => |m| blk: {
            var obj = std.json.ObjectMap.init(allocator);
            for (m) |kv| {
                try obj.put(kv.key, try toJsonValue(allocator, kv.val));
            }
            break :blk .{ .object = obj };
        },
    };
}
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Zig program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Zig(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        'const std = @import("std");\n'
        f"{preamble}\n"
        f"{_TO_JSON_VALUE}"
        "\n"
        "pub fn main() !void {\n"
        f"{result.code}\n"
        "    var arena = std.heap.ArenaAllocator.init(\n"
        "        std.heap.page_allocator,\n"
        "    );\n"
        "    defer arena.deinit();\n"
        f"    const value = try toJsonValue(arena.allocator(), {_VAR_NAME});\n"
        "    const stdout = std.io.getStdOut().writer();\n"
        "    try std.json.stringify(value, .{}, stdout);\n"
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
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
