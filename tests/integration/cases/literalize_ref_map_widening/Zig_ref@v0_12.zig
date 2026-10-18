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
    const string_map: ZVal = .{ .map = &.{
        .{ .key = "k", .val = .{ .str = "s" } },
    }};
    const my_data: ZVal = .{ .arr = &.{
        string_map,
        .{ .map = &.{.{ .key = "k", .val = .{ .int = 1 } }}},
    }};
    _ = my_data;
}
