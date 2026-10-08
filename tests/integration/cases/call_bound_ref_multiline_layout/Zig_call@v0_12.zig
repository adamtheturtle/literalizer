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
    const x: ZVal = .{ .arr = &.{
        .{ .arr = &.{
            .{ .int = 1 },
            .{ .int = 2 },
        }},
        .{ .arr = &.{
            .{ .int = 3 },
            .{ .int = 4 },
        }},
    }};
    f(.{ .arr = &.{
        .{ .arr = &.{
            x,
        }},
    }});
}
