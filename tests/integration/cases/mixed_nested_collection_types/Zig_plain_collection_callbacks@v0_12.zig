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
        .{ .key = "lists", .val = .{ .arr = &.{.{ .arr = &.{.{ .int = 1 }}}, .{ .arr = &.{.{ .str = "x" }}}, .{ .arr = &.{}}}} },
        .{ .key = "maps", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "x", .val = .{ .int = 1 } }}}, .{ .map = &.{.{ .key = "x", .val = .{ .str = "s" } }}}}} },
        .{ .key = "empties", .val = .{ .map = &.{.{ .key = "a", .val = .{ .arr = &.{.{ .int = 1 }}} }, .{ .key = "b", .val = .{ .arr = &.{}} }}} },
    }};
    _ = my_data;
}
