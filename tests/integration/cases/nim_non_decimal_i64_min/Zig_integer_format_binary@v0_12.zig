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
        .{ .int = -0b1000000000000000000000000000000000000000000000000000000000000000 },
        .{ .int = -0b1 },
        .{ .int = 0b111111111111111111111111111111111111111111111111111111111111111 },
    }};
    _ = my_data;
}
