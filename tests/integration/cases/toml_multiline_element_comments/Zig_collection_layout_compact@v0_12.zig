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
        .{ .key = "first", .val = .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }}} },
        .{ .key = "second", .val = .{ .int = 3 } },  // About the second key.
    }};
    _ = my_data;
}
