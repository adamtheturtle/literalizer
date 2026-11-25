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
        .{ .key = "minimum", .val = .{ .int = -0x80000000 } },
        .{ .key = "neighbor", .val = .{ .int = -0x7fffffff } },
        .{ .key = "maximum", .val = .{ .int = 0x7fffffff } },
        .{ .key = "nested", .val = .{ .arr = &.{.{ .int = -0x80000000 }}} },
    }};
    _ = my_data;
}
