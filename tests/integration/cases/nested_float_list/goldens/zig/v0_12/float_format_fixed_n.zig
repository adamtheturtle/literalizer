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
        .{ .arr = &.{.{ .float = 1.500000 }, .{ .float = 2.500000 }}},
        .{ .arr = &.{.{ .float = 3.500000 }, .{ .float = 4.500000 }}},
    }};
    _ = my_data;
}
