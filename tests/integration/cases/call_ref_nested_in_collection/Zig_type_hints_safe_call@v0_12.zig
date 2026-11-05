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
fn process(a: ZVal, b: ZVal) void { _ = a; _ = b; }
pub fn main() void {
    const big_list: ZVal = .{ .arr = &.{
        .{ .str = "x" },
    }};
    process(.{ .map = &.{.{ .key = "k", .val = big_list }}}, .{ .int = 2 });
}
