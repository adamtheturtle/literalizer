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
        .{ .key = "within_i32", .val = .{ .int = 1705320000 } },
        .{ .key = "beyond_i32", .val = .{ .int = 4085195400 } },
    }};
    _ = my_data;
}
