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
fn check(ts: ZVal, d: ZVal) void { _ = ts; _ = d; }
pub fn main() void {
    check(.{ .int = 1705314600 }, .{ .int = 1717200000 });
}
