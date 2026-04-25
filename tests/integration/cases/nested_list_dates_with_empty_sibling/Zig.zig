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
        .{ .arr = &.{.{ .int = 1767225600 }, .{ .int = 1767312000 }}},
        .{ .arr = &.{}},
        .{ .arr = &.{.{ .int = 1770076800 }, .{ .int = 1770163200 }}},
    }};
    _ = my_data;
}
