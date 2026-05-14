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
    var my_data: ZVal = .{ .arr = &.{
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 1 } }, .{ .key = "label", .val = .{ .str = "first" } }}},
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 2 } }, .{ .key = "label", .val = .{ .str = "second" } }}},
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 3 } }, .{ .key = "label", .val = .{ .str = "third" } }}},
    }};
    my_data = .{ .arr = &.{
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 1 } }, .{ .key = "label", .val = .{ .str = "first" } }}},
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 2 } }, .{ .key = "label", .val = .{ .str = "second" } }}},
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 3 } }, .{ .key = "label", .val = .{ .str = "third" } }}},
    }};
    my_data = .nil;
}
