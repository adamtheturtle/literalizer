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
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "times", .val = .{ .arr = &.{.{ .str = "09:30:00" }, .{ .str = "17:45:00" }, .{ .str = "23:59:59" }}} },
    }};
    _ = my_data;
}
