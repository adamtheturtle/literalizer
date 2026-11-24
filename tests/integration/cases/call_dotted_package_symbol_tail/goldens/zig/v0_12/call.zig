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
const HelperType_ = struct { fn list(self: HelperType_, a: ZVal) void { _ = self; _ = a; } };
const helper: HelperType_ = .{};
pub fn main() void {
    helper.list(.{ .int = 1 });
}
