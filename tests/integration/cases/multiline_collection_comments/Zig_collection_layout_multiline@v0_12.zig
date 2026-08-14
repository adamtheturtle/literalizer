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
        .{ .key = "a", .val = .{ .arr = &.{
            .{ .int = 1 },
            .{ .int = 2 },
            .{ .int = 3 },
        }} },  // inline a
        .{ .key = "b", .val = .{ .int = 2 } },  // inline b
    }};
    _ = my_data;
}
