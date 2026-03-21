const ZVal = union(enum) {
    nil,
    bool: bool,
    int: i64,
    float: f64,
    str: []const u8,
    arr: []const ZVal,
    map: []const ZKV,
    set: []const ZVal,
};
const ZKV = struct { key: []const u8, val: ZVal };
pub fn main() void {
    const my_data: ZVal = .{ .arr = &.{
        .{ .str = "2024-01-15T12:30:00+00:00" },
        .{ .str = "2024-06-30T08:00:00+00:00" },
        .{ .str = "2024-12-25T18:45:00+00:00" },
    }};
    _ = my_data;
}
