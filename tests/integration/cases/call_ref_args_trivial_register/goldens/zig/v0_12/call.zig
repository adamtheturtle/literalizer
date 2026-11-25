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
fn process(value: ZVal, count: ZVal) void { _ = value; _ = count; }
pub fn main() void {
    const my_int: ZVal = .{ .int = 1 };
    const my_bool: ZVal = .{ .bool = true };
    const my_float: ZVal = .{ .float = 3.14 };
    const my_list: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
        .{ .int = 3 },
    }};
    process(my_int, .{ .int = 42 });
    process(my_bool, .{ .int = 7 });
    process(my_float, .{ .int = 9 });
    process(my_list, .{ .int = 1 });
}
