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
fn process(data: ZVal, count: ZVal) void { _ = data; _ = count; }
pub fn main() void {
    const shared: ZVal = .{ .int = 1 };
    const other: ZVal = .{ .int = 2 };
    process(shared, .{ .int = 1 });
    process(other, .{ .int = 0 });
    process(shared, .{ .int = 8 });
}
