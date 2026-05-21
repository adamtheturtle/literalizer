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
fn process(a: ZVal, b: ZVal) void { _ = a; _ = b; }
pub fn main() void {
    const my_data = process(.{ .int = 1 }, .{ .int = 2 });
    _ = my_data;
}
