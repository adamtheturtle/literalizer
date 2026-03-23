const ZVal = union(enum) {
    nil,
    bool: bool,
    int: i64,
    float: f64,
    str: []const u8,
    arr: []const ZVal,
    map: []const ZKV,
    set: []const ZVal,
};
const ZKV = struct { key: []const u8, val: ZVal };
pub fn main() void {
    const v: ZVal = .{ .map = &.{
        .{ .key = "a", .val = .{ .map = &.{.{ .key = "x", .val = .{ .int = 1 } }}} },
        .{ .key = "b", .val = .{ .int = 2 } },
    }};
    _ = v;
}
