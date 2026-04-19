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
        .{ .key = "name", .val = .{ .str = "Alice" } },
        .{ .key = "score", .val = .nil },
        .{ .key = "age", .val = .{ .int = 30 } },
    }};
    _ = my_data;
}
