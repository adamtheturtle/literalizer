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
fn process(a: ZVal) void { _ = a; }
pub fn main() void {
    const big_list: ZVal = .{ .arr = &.{
        .{ .str = "x" },
    }};
    process(.{ .map = &.{.{ .key = "m", .val = big_list }}});
}
