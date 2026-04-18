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
    var my_data: ZVal = .{ .set = &.{
        .{ .int = 1705276800 },
        .{ .int = 1717200000 },
    }};
    my_data = .{ .set = &.{
        .{ .int = 1705276800 },
        .{ .int = 1717200000 },
    }};
    my_data = .nil;
}
