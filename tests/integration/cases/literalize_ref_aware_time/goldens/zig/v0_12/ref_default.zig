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
    const shared_time: ZVal = .{ .str = "12:30:15+02:00" };
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "x", .val = shared_time },
    }};
    _ = my_data;
}
