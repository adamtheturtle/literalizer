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
    const foo: ZVal = .{ .map = &.{
        .{ .key = "_", .val = .{ .str = "_" } },
    }};
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "items", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "other", .val = .{ .int = 1 } }}}, foo}} },
        .{ .key = "mapping", .val = .{ .map = &.{.{ .key = "value", .val = foo }}} },
    }};
    _ = my_data;
}
