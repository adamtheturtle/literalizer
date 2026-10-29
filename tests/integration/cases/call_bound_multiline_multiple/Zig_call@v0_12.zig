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
fn f(value: ZVal) void { _ = value; }
pub fn main() void {
    const ref_data: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
    }};
    f(.{ .arr = &.{
        ref_data,
    }});
    f(.{ .arr = &.{
        ref_data,
    }});
}
