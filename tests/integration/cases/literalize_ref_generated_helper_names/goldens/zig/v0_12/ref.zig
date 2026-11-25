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
    const std: ZVal = .{ .map = &.{
        .{ .key = "a", .val = .{ .int = 1 } },
    }};
    const arena: ZVal = .{ .map = &.{
        .{ .key = "a", .val = .{ .int = 1 } },
    }};
    const allocator: ZVal = .{ .map = &.{
        .{ .key = "a", .val = .{ .int = 1 } },
    }};
    const my_data: ZVal = .{ .arr = &.{
        std,
        arena,
        allocator,
    }};
    _ = my_data;
}
