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
fn process(data: ZVal) void { _ = data; }
pub fn main() void {
    const known_value: ZVal = .{ .int = 1 };
    const unknown_value: ZVal = .{ .arr = &.{}};
    process(unknown_value);
}
