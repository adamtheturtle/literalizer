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
        .{ .key = "lower", .val = .{ .int = 3735928559 } },
        .{ .key = "upper", .val = .{ .int = 31 } },
        .{ .key = "negative", .val = .{ .int = -16 } },
        .{ .key = "zero", .val = .{ .int = 0 } },
    }};
    _ = my_data;
}
