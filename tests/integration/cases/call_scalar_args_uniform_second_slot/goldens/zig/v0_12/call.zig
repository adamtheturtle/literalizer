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
fn process(value: ZVal, label: ZVal) void { _ = value; _ = label; }
pub fn main() void {
    process(.{ .str = "hello" }, .{ .str = "a" });
    process(.{ .int = 42 }, .{ .str = "b" });
    process(.{ .bool = true }, .{ .str = "c" });
}
