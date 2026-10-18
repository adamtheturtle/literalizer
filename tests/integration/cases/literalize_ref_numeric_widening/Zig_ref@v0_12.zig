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
    const floating_value: ZVal = .{ .float = 1.5 };
    const integer_value: ZVal = .{ .float = 2.0 };
    const my_data: ZVal = .{ .arr = &.{
        floating_value,
        integer_value,
    }};
    _ = my_data;
}
