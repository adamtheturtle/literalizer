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
fn process(a: ZVal, b: ZVal, c: ZVal, d: ZVal) void { _ = a; _ = b; _ = c; _ = d; }
pub fn main() void {
    process(.{ .int = 1 }, .{ .int = 2 }, .{ .int = 3 }, .{ .int = 4 });
    process(.{ .int = 10 }, .{ .int = 20 }, .{ .int = 30 }, .{ .int = 40 });
}
