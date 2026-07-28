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
fn process(known_value: ZVal, nested_missing: ZVal) void { _ = known_value; _ = nested_missing; }
pub fn main() void {
    const known_value: ZVal = .{ .bool = true };
    const unknown_value: ZVal = .{ .bool = true };
    process(known_value, .{ .arr = &.{unknown_value}});
}
