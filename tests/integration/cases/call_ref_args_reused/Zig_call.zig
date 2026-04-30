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
    const single_var: ZVal = .{ .arr = &.{
        .{ .int = 4 },
        .{ .int = 5 },
        .{ .int = 6 },
    }};
    const repeated_var: ZVal = .{ .int = 1 };
    process(repeated_var, .{ .int = 1 });
    process(single_var, .{ .int = 0 });
    process(repeated_var, .{ .int = 8 });
}
