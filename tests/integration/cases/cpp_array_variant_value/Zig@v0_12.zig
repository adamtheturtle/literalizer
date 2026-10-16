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
        .{ .key = "a", .val = .{ .int = 1 } },
        .{ .key = "b", .val = .{ .str = "x" } },
        .{ .key = "e", .val = .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }}} },
        .{ .key = "f", .val = .{ .map = &.{.{ .key = "g", .val = .{ .str = "h" } }}} },
    }};
    _ = my_data;
}
