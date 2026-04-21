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
        .{ .map = &.{.{ .key = "first", .val = .{ .str = "Alice" } }, .{ .key = "last", .val = .{ .str = "Smith" } }}},
        .{ .map = &.{.{ .key = "first", .val = .{ .str = "Bob" } }, .{ .key = "last", .val = .{ .str = "Jones" } }}},
    }};
    my_data = .{ .arr = &.{
        .{ .map = &.{.{ .key = "first", .val = .{ .str = "Alice" } }, .{ .key = "last", .val = .{ .str = "Smith" } }}},
        .{ .map = &.{.{ .key = "first", .val = .{ .str = "Bob" } }, .{ .key = "last", .val = .{ .str = "Jones" } }}},
    }};
    my_data = .nil;
}
