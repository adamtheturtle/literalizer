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
const LogType_ = struct { fn emit(self: LogType_, _arg: anytype) void { _ = self; _ = _arg; } };
const log: LogType_ = .{};
pub fn main() void {
    log.emit(process(.{ .str = "hello" }));
    log.emit(process(.{ .int = 42 }));
    log.emit(process(.{ .bool = true }));
}
