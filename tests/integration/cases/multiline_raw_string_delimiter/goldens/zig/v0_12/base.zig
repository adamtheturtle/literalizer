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
    const my_data: ZVal = .{ .arr = &.{
        .{ .str = "custom base after empty collision: )\"\nvalue" },
        .{ .str = "custom suffix after base collision: )\" and )x0\"\nvalue" },
        .{ .str = "custom second suffix: )\" and )x0\" and )x00\"\nvalue" },
        .{ .str = "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue" },
    }};
    _ = my_data;
}
