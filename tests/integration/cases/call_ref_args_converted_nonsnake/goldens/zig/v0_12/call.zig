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
fn process(data: ZVal, count: ZVal) void { _ = data; _ = count; }
pub fn main() void {
    const my_var: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
        .{ .int = 3 },
    }};
    const my_other: ZVal = .{ .arr = &.{
        .{ .int = 4 },
        .{ .int = 5 },
        .{ .int = 6 },
    }};
    process(my_var, .{ .int = 42 });
    process(my_other, .{ .int = 7 });
}
