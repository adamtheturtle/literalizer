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
fn consume_widget(_arg: anytype) void { _ = _arg; }
pub fn main() void {
    const item: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
    }};
    const my_data: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
    }};
    consume_widget(my_data);
    my_data = item;
    consume_widget(my_data);
}
