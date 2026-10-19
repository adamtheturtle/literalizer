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
        .{ .key = "alpha", .val = .{ .arr = &.{.{ .int = 2 }, .{ .arr = &.{}}}} },
        .{ .key = "beta", .val = .{ .arr = &.{.{ .int = 5 }, .{ .arr = &.{.{ .str = "x" }}}}} },
    }};
    _ = my_data;
}
