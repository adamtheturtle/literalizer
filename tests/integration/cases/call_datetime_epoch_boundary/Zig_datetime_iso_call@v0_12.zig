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
fn consume(value: ZVal) void { _ = value; }
pub fn main() void {
    consume(.{ .str = "1901-12-13T20:45:51" });
    consume(.{ .str = "2038-01-19T03:14:08" });
}
