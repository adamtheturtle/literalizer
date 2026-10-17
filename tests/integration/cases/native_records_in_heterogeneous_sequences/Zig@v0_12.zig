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
        .{ .key = "h", .val = .{ .arr = &.{.{ .int = 1 }, .{ .str = "a" }, .{ .arr = &.{.{ .int = 2 }, .{ .str = "b" }}}, .{ .map = &.{.{ .key = "k", .val = .{ .arr = &.{.{ .bool = true }}} }}}}} },
    }};
    _ = my_data;
}
