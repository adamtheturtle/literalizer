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
        .{ .key = "outer", .val = .{ .map = &.{.{ .key = "a", .val = .{ .int = 1 } }, .{ .key = "b", .val = .{ .str = "x" } }, .{ .key = "c", .val = .nil }}} },
    }};
    my_data = .{ .map = &.{
        .{ .key = "outer", .val = .{ .map = &.{.{ .key = "a", .val = .{ .int = 1 } }, .{ .key = "b", .val = .{ .str = "x" } }, .{ .key = "c", .val = .nil }}} },
    }};
    my_data = .nil;
}
