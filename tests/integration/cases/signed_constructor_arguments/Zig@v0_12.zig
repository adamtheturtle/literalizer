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
        .{ .int = -42 },
        .{ .int = 0 },
        .{ .int = 42 },
        .{ .float = -1.25 },
        .{ .float = 0.0 },
        .{ .float = 1.25 },
    }};
    _ = my_data;
}
