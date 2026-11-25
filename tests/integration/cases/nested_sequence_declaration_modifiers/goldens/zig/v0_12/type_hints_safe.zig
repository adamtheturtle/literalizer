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
    const my_data: ZVal = .{ .arr = &.{
        .{ .arr = &.{}},
        .{ .arr = &.{.{ .int = 1 }}},
        .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }}},
        .{ .arr = &.{.{ .int = 1 }, .{ .str = "x" }, .{ .bool = true }, .nil}},
        .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }, .{ .int = 3 }, .{ .int = 4 }, .{ .int = 5 }, .{ .int = 6 }, .{ .int = 7 }, .{ .int = 8 }}},
    }};
    _ = my_data;
}
