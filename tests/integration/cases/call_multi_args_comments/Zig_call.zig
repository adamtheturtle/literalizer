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
fn process(ts: ZVal, start: ZVal, end: ZVal) void { _ = ts; _ = start; _ = end; }
pub fn main() void {
    process(.{ .int = 1 }, .{ .int = 0 }, .{ .int = 3600 });  // Jan 1 1970 00:00:00 - 01:00:00
    process(.{ .int = 5 }, .{ .int = 0 }, .{ .int = 3600 });  // Jan 1 1970 00:00:05 - 01:00:05
    process(.{ .int = 2 }, .{ .int = 0 }, .{ .int = 5400 });  // Jan 1 1970 00:00:02 - 01:30:02
}
