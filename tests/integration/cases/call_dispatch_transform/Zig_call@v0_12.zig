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
fn record_value(value: ZVal) void { _ = value; }
fn flush_buffer(count: ZVal) void { _ = count; }
fn emit(_arg: anytype) void { _ = _arg; }
pub fn main() void {
    emit(record_value(.{ .int = 42 }));
    flush_buffer(.{ .int = 3 });
}
