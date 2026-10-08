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
    const empty_values: ZVal = .{ .arr = &.{}};
    const integer_values: ZVal = .{ .arr = &.{
        .{ .int = 1 },
    }};
    const my_data: ZVal = .{ .arr = &.{
        empty_values,
        integer_values,
    }};
    _ = my_data;
}
