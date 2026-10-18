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
        .{ .str = "1901-12-13T20:45:51" },
        .{ .str = "1901-12-13T20:45:52" },
        .{ .str = "2038-01-19T03:14:07" },
        .{ .str = "2038-01-19T03:14:08" },
    }};
    _ = my_data;
}
