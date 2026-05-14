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
const TracerType_ = struct { fn emit(self: TracerType_, _arg: anytype) void { _ = self; _ = _arg; } };
const tracer: TracerType_ = .{};
pub fn main() void {
    tracer.emit(process(.{ .str = "hello" }));
    tracer.emit(process(.{ .int = 42 }));
    tracer.emit(process(.{ .bool = true }));
}
