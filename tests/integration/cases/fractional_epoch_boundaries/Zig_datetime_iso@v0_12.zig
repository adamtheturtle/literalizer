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
        .{ .str = "1970-01-01T00:00:00.000001+00:00" },
        .{ .str = "1969-12-31T23:59:59.500000+00:00" },
        .{ .str = "1970-01-01T00:00:01+00:00" },
    }};
    _ = my_data;
}
