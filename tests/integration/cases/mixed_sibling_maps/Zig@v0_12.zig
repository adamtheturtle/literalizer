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
        .{ .arr = &.{.{ .map = &.{.{ .key = "a", .val = .{ .int = 1 } }}}, .{ .map = &.{.{ .key = "a", .val = .nil }}}, .{ .int = 42 }}},
        .{ .arr = &.{.{ .map = &.{.{ .key = "a", .val = .{ .int = 1 } }}}, .{ .map = &.{.{ .key = "a", .val = .{ .str = "s" } }}}, .{ .int = 42 }}},
        .{ .arr = &.{.{ .map = &.{.{ .key = "a", .val = .{ .int = 1 } }}}, .{ .map = &.{.{ .key = "a", .val = .nil }}}}},
        .{ .arr = &.{.{ .map = &.{.{ .key = "a", .val = .{ .int = 1 } }}}, .{ .map = &.{.{ .key = "a", .val = .{ .str = "s" } }}}}},
    }};
    _ = my_data;
}
