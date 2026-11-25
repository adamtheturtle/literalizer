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
        .{ .int = 42 },
        .{ .float = 3.14 },
        .{ .bool = true },
        .{ .bool = false },
        .{ .str = "hello \"world\"" },
    }};
    _ = my_data;
}
