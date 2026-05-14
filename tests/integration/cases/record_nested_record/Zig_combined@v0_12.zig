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
        .{ .key = "id", .val = .{ .int = 1 } },
        .{ .key = "owner", .val = .{ .map = &.{.{ .key = "name", .val = .{ .str = "Alice" } }, .{ .key = "age", .val = .{ .int = 30 } }}} },
    }};
    my_data = .{ .map = &.{
        .{ .key = "id", .val = .{ .int = 1 } },
        .{ .key = "owner", .val = .{ .map = &.{.{ .key = "name", .val = .{ .str = "Alice" } }, .{ .key = "age", .val = .{ .int = 30 } }}} },
    }};
    my_data = .nil;
}
