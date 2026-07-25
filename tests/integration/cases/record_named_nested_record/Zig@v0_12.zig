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
        .{ .key = "collection", .val = .{ .str = "alpha" } },
        .{ .key = "featured_entry", .val = .{ .map = &.{.{ .key = "id", .val = .{ .int = 100 } }, .{ .key = "label", .val = .{ .str = "first entry" } }, .{ .key = "enabled", .val = .{ .bool = false } }, .{ .key = "related_ids", .val = .{ .arr = &.{.{ .int = 102 }, .{ .int = 103 }}} }}} },
    }};
    _ = my_data;
}
