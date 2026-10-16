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
    const my_data: ZVal = .{ .arr = &.{
        .{ .map = &.{.{ .key = "type", .val = .{ .str = "create" } }, .{ .key = "name", .val = .{ .str = "a" } }}},
        .{ .map = &.{.{ .key = "type", .val = .{ .str = "update" } }, .{ .key = "name", .val = .{ .str = "b" } }}},
    }};
    _ = my_data;
}
