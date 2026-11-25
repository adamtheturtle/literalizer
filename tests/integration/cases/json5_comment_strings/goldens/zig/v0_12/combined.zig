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
        // strings stay data
        .{ .str = "https://example.org/a/*b*/" },  // URL annotation
        .{ .str = "escaped quote: \" // still data" },
        .{ .str = "backslash: \\" },  // outside the string
        .{ .str = "/* not a comment */" },
    }};
    my_data = .{ .arr = &.{
        // strings stay data
        .{ .str = "https://example.org/a/*b*/" },  // URL annotation
        .{ .str = "escaped quote: \" // still data" },
        .{ .str = "backslash: \\" },  // outside the string
        .{ .str = "/* not a comment */" },
    }};
    my_data = .nil;
}
