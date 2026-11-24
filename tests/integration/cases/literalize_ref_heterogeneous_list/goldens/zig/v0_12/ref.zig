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
    const one: ZVal = .{ .int = 1 };
    const two: ZVal = .{ .str = "s" };
    const my_data: ZVal = .{ .arr = &.{
        one,
        two,
    }};
    _ = my_data;
}
