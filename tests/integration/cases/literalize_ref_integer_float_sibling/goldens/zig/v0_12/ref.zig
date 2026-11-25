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
    const integer_value: ZVal = .{ .float = 1.0 };
    const my_data: ZVal = .{ .arr = &.{
        integer_value,
        .{ .float = 1.5 },
    }};
    _ = my_data;
}
