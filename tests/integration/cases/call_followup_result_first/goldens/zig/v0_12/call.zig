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
fn make_widget(first: ZVal, second: ZVal) ZVal { _ = first; _ = second; return .nil; }
fn consume(first: ZVal, second: ZVal) void { _ = first; _ = second; }
pub fn main() void {
    const my_data = make_widget(.{ .int = 42 }, .{ .int = 3 });
    consume(my_data, .{ .int = 3 });
}
