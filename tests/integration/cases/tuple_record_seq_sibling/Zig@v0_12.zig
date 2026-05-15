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
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "scores", .val = .{ .arr = &.{.{ .int = 10 }, .{ .int = 20 }, .{ .int = 30 }}} },
        .{ .key = "args", .val = .{ .arr = &.{.{ .int = 1 }, .{ .str = "email" }, .{ .str = "a@gmail.com" }, .{ .int = 100 }}} },
    }};
    _ = my_data;
}
