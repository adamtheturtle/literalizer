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
        .{ .key = "single_map", .val = .{ .arr = &.{.{ .map = &.{}}}} },
        .{ .key = "single_list", .val = .{ .arr = &.{.{ .arr = &.{.{ .int = 1 }}}}} },
        .{ .key = "single_deep", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .int = 2 }}}}}}} },
    }};
    _ = my_data;
}
