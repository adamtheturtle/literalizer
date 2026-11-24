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
        .{ .arr = &.{.{ .int = 2 }, .{ .str = "hello" }}},  // trailing note
        // next element
        .{ .arr = &.{.{ .int = 3 }, .{ .str = "world" }}},
    }};
    my_data = .{ .arr = &.{
        .{ .arr = &.{.{ .int = 2 }, .{ .str = "hello" }}},  // trailing note
        // next element
        .{ .arr = &.{.{ .int = 3 }, .{ .str = "world" }}},
    }};
    my_data = .nil;
}
