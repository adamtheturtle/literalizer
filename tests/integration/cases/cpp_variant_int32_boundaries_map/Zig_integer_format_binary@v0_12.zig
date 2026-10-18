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
        .{ .key = "below", .val = .{ .int = -0b10000000000000000000000000000001 } },
        .{ .key = "minimum", .val = .{ .int = -0b10000000000000000000000000000000 } },
        .{ .key = "above", .val = .{ .int = -0b1111111111111111111111111111111 } },
        .{ .key = "nested", .val = .{ .arr = &.{.{ .int = 0b0 }}} },
    }};
    _ = my_data;
}
