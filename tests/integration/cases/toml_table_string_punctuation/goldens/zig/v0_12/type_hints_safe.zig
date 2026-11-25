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
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "comma_hash", .val = .{ .str = "a,#b" } },
        .{ .key = "comma_space_hash", .val = .{ .str = "trail, # comment" } },
        .{ .key = "escaped_quote", .val = .{ .str = "quote \" and , #" } },
        .{ .key = "next_line", .val = .{ .str = "x    y" } },
        .{ .key = "line_separator", .val = .{ .str = "x     y" } },
        .{ .key = "paragraph_separator", .val = .{ .str = "x     y" } },
    }};
    _ = my_data;
}
