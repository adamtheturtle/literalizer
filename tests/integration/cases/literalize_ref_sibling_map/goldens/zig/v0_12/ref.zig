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
    const sibling_map: ZVal = .{ .map = &.{
        .{ .key = "k", .val = .{ .int = 2 } },
    }};
    const my_data: ZVal = .{ .arr = &.{
        .{ .map = &.{.{ .key = "k", .val = .{ .int = 1 } }}},
        sibling_map,
    }};
    _ = my_data;
}
