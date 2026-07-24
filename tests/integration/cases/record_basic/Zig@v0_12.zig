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
        .{ .key = "id", .val = .{ .int = 1 } },
        .{ .key = "label", .val = .{ .str = "She said \"hello\", then waved" } },
        .{ .key = "enabled", .val = .{ .bool = false } },
        .{ .key = "related_ids", .val = .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }, .{ .int = 3 }}} },
    }};
    _ = my_data;
}
