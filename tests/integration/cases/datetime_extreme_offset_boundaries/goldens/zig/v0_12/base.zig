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
        .{ .int = 1592308740 },
        .{ .int = 1592287200 },
        .{ .int = 1592157600 },
        .{ .int = 1592136060 },
    }};
    _ = my_data;
}
