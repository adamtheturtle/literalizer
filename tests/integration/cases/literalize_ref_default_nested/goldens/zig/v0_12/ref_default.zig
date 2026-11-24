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
    const item_var: ZVal = .{ .map = &.{
        .{ .key = "_", .val = .{ .str = "_" } },
    }};
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "items", .val = .{ .arr = &.{item_var, .{ .map = &.{.{ .key = "fallback", .val = .{ .str = "value" } }}}}} },
    }};
    _ = my_data;
}
