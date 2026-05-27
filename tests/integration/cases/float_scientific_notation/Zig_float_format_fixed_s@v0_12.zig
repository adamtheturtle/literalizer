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
        .{ .float = 0.000000 },
        .{ .float = 1.000000 },
        .{ .float = 1500.000000 },
        .{ .float = 0.001000 },
        .{ .float = 10000000000000000.000000 },
    }};
    _ = my_data;
}
