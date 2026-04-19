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
        .{ .arr = &.{.{ .map = &.{.{ .key = "name", .val = .{ .str = "Alice" } }}}, .{ .map = &.{.{ .key = "name", .val = .{ .str = "Bob" } }}}}},
        .{ .arr = &.{.{ .map = &.{.{ .key = "name", .val = .{ .str = "Charlie" } }}}, .{ .map = &.{.{ .key = "name", .val = .{ .str = "Dave" } }}}}},
    }};
    my_data = .{ .arr = &.{
        .{ .arr = &.{.{ .map = &.{.{ .key = "name", .val = .{ .str = "Alice" } }}}, .{ .map = &.{.{ .key = "name", .val = .{ .str = "Bob" } }}}}},
        .{ .arr = &.{.{ .map = &.{.{ .key = "name", .val = .{ .str = "Charlie" } }}}, .{ .map = &.{.{ .key = "name", .val = .{ .str = "Dave" } }}}}},
    }};
    my_data = .nil;
}
