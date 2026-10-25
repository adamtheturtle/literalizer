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
fn consume_widget(arg_value: ZVal) void { _ = arg_value; }
pub fn main() void {
    const item: ZVal = .{ .arr = &.{}};
    const my_data: ZVal = .{ .arr = &.{
        item,
        item,
    }};
    consume_widget(my_data);
}
