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
fn make_widget(count: ZVal) ZVal { _ = count; return .nil; }
pub fn main() void {
    var my_data = make_widget(.{ .int = 42 });
    my_data = (~/\;//).match("/") ? make_widget(.{ .int = 42 }) : null // trailing
    _ = &my_data;
}
