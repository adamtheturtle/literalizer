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
fn consume(items: ZVal, mapping: ZVal) void { _ = items; _ = mapping; }
pub fn main() void {
    const foo: ZVal = .{ .int = 42 };
    consume(.{ .arr = &.{
        .{ .map = &.{
            .{ .key = "other", .val = .{ .int = 1 } },
        }},
        foo,
    }}, .{ .map = &.{
        .{ .key = "left", .val = foo },
        .{ .key = "other", .val = .{ .int = 1 } },
    }});
}
