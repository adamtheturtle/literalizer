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
const ThrottlerType_ = struct { fn check(self: ThrottlerType_, user_id: ZVal, ts: ZVal) void { _ = self; _ = user_id; _ = ts; } };
const throttler: ThrottlerType_ = .{};
fn emit(_arg: anytype) void { _ = _arg; }
pub fn main() void {
    emit(throttler.check(.{ .str = "user_1" }, .{ .float = 1000.0 }));
    emit(throttler.check(.{ .str = "user_2" }, .{ .float = 2000.5 }));
}
