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
fn process(value: ZVal) void { _ = value; }
pub fn main() void {
    process(.{ .str = "09:30:00" });
    process(.{ .int = 1705276800 });
    process(.{ .int = 1 });
}
