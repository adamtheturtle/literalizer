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
        .{ .key = "b", .val = .nil },
        .{ .key = "a", .val = .{ .map = &.{.{ .key = "y", .val = .{ .arr = &.{.{ .float = 1.0 }}} }, .{ .key = "x", .val = .{ .bool = false } }}} },
    }};
    _ = my_data;
}
