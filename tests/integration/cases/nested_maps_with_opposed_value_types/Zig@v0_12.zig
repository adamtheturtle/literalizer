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
    const my_data: ZVal = .{ .arr = &.{
        .{ .map = &.{.{ .key = "input", .val = .{ .map = &.{.{ .key = "name", .val = .{ .str = "alice" } }, .{ .key = "city", .val = .{ .str = "paris" } }}} }, .{ .key = "expected", .val = .{ .map = &.{.{ .key = "count", .val = .{ .int = 1 } }, .{ .key = "total", .val = .{ .int = 2 } }}} }}},
        .{ .map = &.{.{ .key = "input", .val = .{ .map = &.{.{ .key = "name", .val = .{ .int = 10 } }, .{ .key = "city", .val = .{ .int = 20 } }}} }, .{ .key = "expected", .val = .{ .map = &.{.{ .key = "count", .val = .{ .str = "done" } }, .{ .key = "total", .val = .{ .str = "pending" } }}} }}},
    }};
    _ = my_data;
}
