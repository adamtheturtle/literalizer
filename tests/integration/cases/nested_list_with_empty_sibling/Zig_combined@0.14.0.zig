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
    var my_data: ZVal = .{ .arr = &.{
        .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }}},
        .{ .arr = &.{}},
        .{ .arr = &.{.{ .int = 3 }, .{ .int = 4 }}},
    }};
    my_data = .{ .arr = &.{
        .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }}},
        .{ .arr = &.{}},
        .{ .arr = &.{.{ .int = 3 }, .{ .int = 4 }}},
    }};
    my_data = .nil;
}
