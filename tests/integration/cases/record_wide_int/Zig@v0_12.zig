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
        .{ .key = "quantity", .val = .{ .int = 1000000 } },
        .{ .key = "big", .val = .{ .uint = 18446744073709551615 } },
        .{ .key = "ratio", .val = .{ .float = 2.5 } },
        .{ .key = "label", .val = .{ .str = "tag" } },
        .{ .key = "ok", .val = .{ .bool = true } },
    }};
    _ = my_data;
}
