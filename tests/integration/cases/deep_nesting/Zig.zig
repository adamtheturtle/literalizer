const ZDate = struct { year: i32, month: u8, day: u8 };
const ZDatetime = struct { year: i32, month: u8, day: u8, hour: u8, minute: u8, second: u8 };
const ZVal = union(enum) {
    nil,
    bool: bool,
    int: i64,
    float: f64,
    str: []const u8,
    arr: []const ZVal,
    map: []const ZKV,
    set: []const ZVal,
    date: ZDate,
    datetime: ZDatetime,
};
const ZKV = struct { key: []const u8, val: ZVal };
pub fn main() void {
    const v: ZVal = .{ .map = &.{
        .{ .key = "level1", .val = .{ .map = &.{.{ .key = "level2", .val = .{ .map = &.{.{ .key = "level3", .val = .{ .map = &.{.{ .key = "level4", .val = .{ .map = &.{.{ .key = "value", .val = .{ .str = "deep" } }, .{ .key = "items", .val = .{ .arr = &.{.{ .str = "a" }, .{ .str = "b" }}} }}} }}} }, .{ .key = "sibling", .val = .{ .int = 42 } }}} }, .{ .key = "tags", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "name", .val = .{ .str = "tag1" } }, .{ .key = "meta", .val = .{ .map = &.{.{ .key = "priority", .val = .{ .int = 1 } }, .{ .key = "labels", .val = .{ .arr = &.{.{ .str = "x" }, .{ .str = "y" }}} }}} }}}}} }}} },
    }};
    _ = v;
}
