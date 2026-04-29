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
    const val_x: ZVal = .{ .map = &.{
        .{ .key = "_", .val = .{ .str = "_" } },
    }};
    const val_y: ZVal = .{ .map = &.{
        .{ .key = "_", .val = .{ .str = "_" } },
    }};
    const my_data: ZVal = .{ .arr = &.{
        val_x,
        val_y,
    }};
    _ = my_data;
}
