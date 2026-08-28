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
fn record_entry(s: ZVal, n: ZVal, b: ZVal) void { _ = s; _ = n; _ = b; }
pub fn main() void {
    const my_data = record_entry(.{ .str = "a" }, .{ .int = 1 }, .{ .bool = true });
    _ = my_data;
}
