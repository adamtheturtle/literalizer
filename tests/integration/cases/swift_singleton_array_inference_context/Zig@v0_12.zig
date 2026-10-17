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
        .{ .key = "nil", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.nil}}}}}}}}}}}}}}}}}} },
        .{ .key = "empty", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{}}}}}}}}}}}}}}}}}}}} },
        .{ .key = "siblings", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .int = 4 }, .{ .int = 5 }}}}}}}}}}}}}}}}}}}}} },
    }};
    _ = my_data;
}
