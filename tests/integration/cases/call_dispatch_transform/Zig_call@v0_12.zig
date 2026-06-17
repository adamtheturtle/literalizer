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
fn record(value: ZVal) void { _ = value; }
fn flush(count: ZVal) void { _ = count; }
pub fn main() void {
    record(.{ .int = 42 });
    flush(.{ .int = 3 });
}
