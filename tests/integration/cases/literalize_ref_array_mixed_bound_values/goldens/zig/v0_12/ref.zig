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
    const array_value: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
    }};
    const scalar_value: ZVal = .{ .int = 3 };
    const my_data: ZVal = .{ .arr = &.{
        array_value,
        scalar_value,
    }};
    _ = my_data;
}
