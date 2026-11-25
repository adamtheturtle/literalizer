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
    var my_data: ZVal = .{ .map = &.{
        .{ .key = "lint", .val = .{ .arr = &.{.{ .int = 2 }, .{ .arr = &.{.{ .int = 1 }}}}} },
        .{ .key = "test", .val = .{ .arr = &.{.{ .int = 5 }, .{ .arr = &.{.{ .int = 7 }}}}} },
    }};
    my_data = .{ .map = &.{
        .{ .key = "lint", .val = .{ .arr = &.{.{ .int = 2 }, .{ .arr = &.{.{ .int = 1 }}}}} },
        .{ .key = "test", .val = .{ .arr = &.{.{ .int = 5 }, .{ .arr = &.{.{ .int = 7 }}}}} },
    }};
    my_data = .nil;
}
