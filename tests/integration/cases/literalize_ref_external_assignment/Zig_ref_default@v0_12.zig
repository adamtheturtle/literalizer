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
    const ref_data: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
    }};
    var my_data: ZVal = .{ .arr = &.{
        .{ .int = 0 },
    }};
    consume_widget(my_data);
    my_data = ref_data;
    consume_widget(my_data);
    _ = &my_data;
}
