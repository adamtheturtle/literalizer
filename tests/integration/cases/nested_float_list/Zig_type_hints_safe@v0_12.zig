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
        .{ .arr = &.{.{ .float = 1.5 }, .{ .float = 2.5 }}},
        .{ .arr = &.{.{ .float = 3.5 }, .{ .float = 4.5 }}},
    }};
    _ = my_data;
}
