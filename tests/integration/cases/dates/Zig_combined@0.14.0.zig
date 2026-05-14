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
    var my_data: ZVal = .{ .map = &.{
        .{ .key = "date", .val = .{ .int = 1705276800 } },
        .{ .key = "datetime", .val = .{ .int = 1705321800 } },
    }};
    my_data = .{ .map = &.{
        .{ .key = "date", .val = .{ .int = 1705276800 } },
        .{ .key = "datetime", .val = .{ .int = 1705321800 } },
    }};
    my_data = .nil;
}
