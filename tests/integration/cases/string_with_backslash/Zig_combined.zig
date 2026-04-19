const ZVal = union(enum) {
    nil,
    bool: bool,
    int: i64,
    uint: u64,
    float: f64,
    str: []const u8,
    arr: []const ZVal,
    map: []const ZKV,
    set: []const ZVal,
};
const ZKV = struct { key: []const u8, val: ZVal };
pub fn main() void {
    var my_data: ZVal = .{ .arr = &.{
        .{ .str = "C:\\path\\to\\file" },
        .{ .str = "back\\\\slash" },
        .{ .str = "hello \\\"world\\\"" },
        .{ .str = "path\\to \"# file" },
        .{ .str = "trailing\\" },
        .{ .str = "both \"quotes''' here" },
        .{ .str = "line1\\nline2\nwith newline" },
    }};
    my_data = .{ .arr = &.{
        .{ .str = "C:\\path\\to\\file" },
        .{ .str = "back\\\\slash" },
        .{ .str = "hello \\\"world\\\"" },
        .{ .str = "path\\to \"# file" },
        .{ .str = "trailing\\" },
        .{ .str = "both \"quotes''' here" },
        .{ .str = "line1\\nline2\nwith newline" },
    }};
    my_data = .nil;
}
