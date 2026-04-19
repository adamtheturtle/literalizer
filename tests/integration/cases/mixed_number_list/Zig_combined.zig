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
    var my_data: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .float = 2.5 },
        .{ .int = 3 },
    }};
    my_data = .{ .arr = &.{
        .{ .int = 1 },
        .{ .float = 2.5 },
        .{ .int = 3 },
    }};
    my_data = .nil;
}
