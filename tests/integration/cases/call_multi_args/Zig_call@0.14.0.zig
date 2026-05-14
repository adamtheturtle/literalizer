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
fn process(value: ZVal, count: ZVal) void { _ = value; _ = count; }
pub fn main() void {
    process(.{ .int = 1 }, .{ .int = 42 });
    process(.{ .int = 2 }, .{ .int = 100 });
}
