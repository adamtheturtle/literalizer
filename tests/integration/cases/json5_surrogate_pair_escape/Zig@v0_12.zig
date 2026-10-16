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
        .{ .key = "astral", .val = .{ .str = "😀" } },
        .{ .key = "mixed", .val = .{ .str = "a😀b" } },
        .{ .key = "count", .val = .{ .int = 2 } },
        .{ .key = "list", .val = .{ .arr = &.{.{ .str = "😀" }, .{ .int = 1 }}} },
        .{ .key = "nested", .val = .{ .map = &.{.{ .key = "inner", .val = .{ .str = "😀" } }}} },
    }};
    _ = my_data;
}
