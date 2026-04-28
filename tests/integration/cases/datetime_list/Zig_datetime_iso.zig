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
        .{ .str = "2024-01-15T12:30:00.123456+00:00" },
        .{ .str = "2024-06-01T08:00:00+00:00" },
    }};
    _ = my_data;
}
