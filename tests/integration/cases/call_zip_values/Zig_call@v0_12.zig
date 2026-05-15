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
fn process(value: ZVal) void { _ = value; }
fn emit(_call: ZVal, _zip: ZVal) void { _ = _call; _ = _zip; }
pub fn main() void {
    emit(process(.{ .str = "hello" }), .{ .bool = true });
    emit(process(.{ .int = 42 }), .{ .bool = false });
}
