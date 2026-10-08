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
        .{ .key = "first", .val = .{ .map = &.{.{ .key = "x", .val = .{ .int = 1 } }, .{ .key = "y", .val = .{ .int = 2 } }}} },
        .{ .key = "second", .val = .{ .map = &.{.{ .key = "z", .val = .{ .int = 3 } }}} },
    }};
    _ = my_data;
}
