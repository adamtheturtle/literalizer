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
fn process(xs: ZVal) void { _ = xs; }
pub fn main() void {
    process(.{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
    }});
    process(.{ .arr = &.{
        .{ .int = 3 },
    }});
}
