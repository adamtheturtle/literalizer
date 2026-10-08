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
fn f(x: ZVal, _x: ZVal) void { _ = x; _ = _x; }
pub fn main() void {
    f(.{ .int = 1 }, .{ .int = 2 });
}
