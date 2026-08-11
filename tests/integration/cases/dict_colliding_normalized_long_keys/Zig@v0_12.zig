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
        .{ .key = "a_b", .val = .{ .int = 1 } },
        .{ .key = "a-b", .val = .{ .int = 2 } },
        .{ .key = "averyveryverylongkeynamethatgoesonandonandon", .val = .{ .int = 3 } },
        .{ .key = "averyveryverylongkeynamethatgoesonandmore", .val = .{ .int = 4 } },
    }};
    _ = my_data;
}
