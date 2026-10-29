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
        // before<U+0009>line
        .{ .key = "value", .val = .{ .str = "left\tright" } },  // inline<U+0009>line
        // after<U+0009>line
    }};
    _ = my_data;
}
