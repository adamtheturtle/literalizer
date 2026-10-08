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
        .{ .key = "naive", .val = .{ .int = -62135551800 } },
        .{ .key = "recent", .val = .{ .int = 1716804000 } },
    }};
    _ = my_data;
}
