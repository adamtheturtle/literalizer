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
const ThrottlerType_ = struct { fn check(self: ThrottlerType_) void { _ = self; } };
const throttler: ThrottlerType_ = .{};
pub fn main() void {
    throttler.check();
    throttler.check();
}
