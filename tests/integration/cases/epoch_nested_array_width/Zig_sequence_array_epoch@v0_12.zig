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
        .{ .key = "positive", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "item", .val = .{ .arr = &.{.{ .int = 2147483648 }}} }}}}} },
        .{ .key = "negative", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "item", .val = .{ .arr = &.{.{ .int = -2147483649 }}} }}}}} },
        .{ .key = "mixed", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "item", .val = .{ .arr = &.{.{ .int = 0 }, .{ .int = 2147483648 }}} }}}}} },
    }};
    _ = my_data;
}
