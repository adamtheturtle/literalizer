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
        .{ .key = "del", .val = .{ .str = "a\x7fb" } },
        .{ .key = "nel", .val = .{ .str = "a    b" } },
        .{ .key = "c1", .val = .{ .str = "ab" } },
    }};
    _ = my_data;
}
