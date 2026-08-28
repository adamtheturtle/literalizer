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
        .{ .key = "flow", .val = .{ .arr = &.{
            .{ .int = 1 },
            // After the first element.
            .{ .int = 2 },
        }} },
        // Between the key and its value.
        .{ .key = "gap", .val = .{ .int = 3 } },
        // On the block scalar header.
        .{ .key = "block", .val = .{ .str = "Text.\n" } },
        .{ .key = "anchored", .val = .{ .int = 4 } },
        .{ .key = "alias", .val = .{ .int = 4 } },
        // On the alias.
    }};
    _ = my_data;
}
