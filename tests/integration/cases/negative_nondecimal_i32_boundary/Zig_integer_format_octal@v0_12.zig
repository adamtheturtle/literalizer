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
        .{ .key = "minimum", .val = .{ .int = -0o20000000000 } },
        .{ .key = "below", .val = .{ .int = -0o26264057000 } },
    }};
    _ = my_data;
}
