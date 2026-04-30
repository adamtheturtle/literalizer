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
        .{ .arr = &.{.{ .map = &.{.{ .key = "$ref", .val = .{ .str = "repeated_var" } }}}, .{ .int = 1 }}},
        .{ .arr = &.{.{ .map = &.{.{ .key = "$ref", .val = .{ .str = "single_var" } }}}, .{ .int = 0 }}},
        .{ .arr = &.{.{ .map = &.{.{ .key = "$ref", .val = .{ .str = "repeated_var" } }}}, .{ .int = 8 }}},
    }};
    _ = my_data;
}
