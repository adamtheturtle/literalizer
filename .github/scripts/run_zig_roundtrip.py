"""Zig JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Zig
``const myData: ZVal = ...`` declaration, wrap it in a tiny ``main``
that serializes ``myData`` back to JSON via a small recursive helper,
run it with ``zig run``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

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

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Zig

_VAR_NAME = "myData"
_LABEL = "Zig"
_EXCLUDED_KEYS = ("biginteger",)

# Recursive ZVal -> JSON writer. ``.arr`` and ``.set`` share the
# ``[]const ZVal`` payload type, so a single switch prong handles both;
# ``.nil`` never appears in the shared input (it is ``null``-free) but
# the union is exhaustive so the prong is required.
_WRITE_JSON = r"""
fn writeJsonString(writer: anytype, s: []const u8) !void {
    try writer.writeByte('"');
    for (s) |c| {
        switch (c) {
            '"' => try writer.writeAll("\\\""),
            '\\' => try writer.writeAll("\\\\"),
            '\n' => try writer.writeAll("\\n"),
            '\r' => try writer.writeAll("\\r"),
            '\t' => try writer.writeAll("\\t"),
            0x08 => try writer.writeAll("\\b"),
            0x0c => try writer.writeAll("\\f"),
            else => {
                if (c < 0x20) {
                    try std.fmt.format(writer, "\\u{x:0>4}", .{c});
                } else {
                    try writer.writeByte(c);
                }
            },
        }
    }
    try writer.writeByte('"');
}

fn writeJson(writer: anytype, v: ZVal) !void {
    switch (v) {
        .nil => try writer.writeAll("null"),
        .bool => |b| try writer.writeAll(if (b) "true" else "false"),
        .int => |i| try std.fmt.format(writer, "{d}", .{i}),
        .uint => |u| try std.fmt.format(writer, "{d}", .{u}),
        .float => |f| try std.fmt.format(writer, "{e}", .{f}),
        .str => |s| try writeJsonString(writer, s),
        .arr, .set => |a| {
            try writer.writeByte('[');
            for (a, 0..) |item, i| {
                if (i > 0) try writer.writeByte(',');
                try writeJson(writer, item);
            }
            try writer.writeByte(']');
        },
        .map => |m| {
            try writer.writeByte('{');
            for (m, 0..) |kv, i| {
                if (i > 0) try writer.writeByte(',');
                try writeJsonString(writer, kv.key);
                try writer.writeByte(':');
                try writeJson(writer, kv.val);
            }
            try writer.writeByte('}');
        },
    }
}
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Zig program literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Zig(),
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        'const std = @import("std");\n'
        f"{preamble}\n"
        "\n"
        f"{_WRITE_JSON}"
        "\n"
        "pub fn main() !void {\n"
        f"{result.code}\n"
        "    const stdout = std.io.getStdOut().writer();\n"
        f"    try writeJson(stdout, {_VAR_NAME});\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Zig backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    zig = shutil.which(cmd="zig") or "zig"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        (tmpdir / "main.zig").write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[zig, "run", "main.zig"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: zig run error\n{run_result.stdout}{run_result.stderr}",
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
