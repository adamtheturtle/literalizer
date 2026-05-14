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
        .{ .key = "host", .val = .{ .str = "localhost" } },
        .{ .key = "port", .val = .nil },  // not configured yet
        .{ .key = "debug", .val = .{ .bool = true } },
    }};
    _ = my_data;
}
