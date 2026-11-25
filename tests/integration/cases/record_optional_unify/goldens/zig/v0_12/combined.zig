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
        .{ .key = "items", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "id", .val = .{ .int = 1 } }}}, .{ .map = &.{.{ .key = "id", .val = .{ .int = 2 } }, .{ .key = "count", .val = .{ .int = 10 } }}}, .{ .map = &.{.{ .key = "id", .val = .{ .int = 3 } }, .{ .key = "count", .val = .{ .int = 20 } }}}}} },
    }};
    my_data = .{ .map = &.{
        .{ .key = "items", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "id", .val = .{ .int = 1 } }}}, .{ .map = &.{.{ .key = "id", .val = .{ .int = 2 } }, .{ .key = "count", .val = .{ .int = 10 } }}}, .{ .map = &.{.{ .key = "id", .val = .{ .int = 3 } }, .{ .key = "count", .val = .{ .int = 20 } }}}}} },
    }};
    my_data = .nil;
}
