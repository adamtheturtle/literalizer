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
        .{ .key = "morning", .val = "09:30:00" },
        .{ .key = "afternoon", .val = "14:15:00" },
        .{ .key = "evening", .val = "23:59:59" },
    }};
    my_data = .{ .map = &.{
        .{ .key = "morning", .val = "09:30:00" },
        .{ .key = "afternoon", .val = "14:15:00" },
        .{ .key = "evening", .val = "23:59:59" },
    }};
    my_data = .nil;
}
