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
    var shared: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
    }};
    var second: ZVal = .{ .arr = &.{
        .{ .int = 3 },
        .{ .int = 4 },
    }};
    var my_data: ZVal = .{ .arr = &.{
        shared,
        second,
    }};
    _ = &shared;
    _ = &second;
    my_data = .nil;
}
