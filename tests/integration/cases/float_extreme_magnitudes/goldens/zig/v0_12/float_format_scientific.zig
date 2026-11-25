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
        .{ .float = 5.0e-324 },
        .{ .float = 2.2250738585072014e-308 },
        .{ .float = 1.0e-307 },
        .{ .float = 1.0e21 },
        .{ .float = -1.5e300 },
        .{ .float = 1.7976931348623157e308 },
        .{ .float = -1.7976931348623157e308 },
    }};
    _ = my_data;
}
