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
        .{ .key = "date", .val = .{ .int = -59030380800 } },
        .{ .key = "naive", .val = .{ .str = "0001-01-01T12:30:00" } },
        .{ .key = "recent", .val = .{ .str = "2024-05-27T10:00:00" } },
    }};
    _ = my_data;
}
