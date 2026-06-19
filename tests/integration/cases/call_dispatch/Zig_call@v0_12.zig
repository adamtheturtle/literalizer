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
fn store_item(key: ZVal, value: ZVal) void { _ = key; _ = value; }
fn read_item(key: ZVal) void { _ = key; }
pub fn main() void {
    store_item(.{ .int = 1 }, .{ .int = 10 });
    read_item(.{ .int = 1 });
}
