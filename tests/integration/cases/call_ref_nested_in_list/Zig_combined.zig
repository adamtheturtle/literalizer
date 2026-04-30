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
        .{ .arr = &.{.{ .arr = &.{.{ .map = &.{.{ .key = "$ref", .val = .{ .str = "my_var" } }}}, .{ .int = 42 }, .{ .str = "static" }}}}},
        .{ .arr = &.{.{ .arr = &.{.{ .map = &.{.{ .key = "$ref", .val = .{ .str = "my_other" } }}}, .{ .int = 7 }, .{ .str = "label" }}}}},
    }};
    my_data = .{ .arr = &.{
        .{ .arr = &.{.{ .arr = &.{.{ .map = &.{.{ .key = "$ref", .val = .{ .str = "my_var" } }}}, .{ .int = 42 }, .{ .str = "static" }}}}},
        .{ .arr = &.{.{ .arr = &.{.{ .map = &.{.{ .key = "$ref", .val = .{ .str = "my_other" } }}}, .{ .int = 7 }, .{ .str = "label" }}}}},
    }};
    my_data = .nil;
}
