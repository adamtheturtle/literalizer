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
const ApiType_ = struct { fn process(self: ApiType_, self: ZVal) void { _ = self; _ = self; } };
const api: ApiType_ = .{};
pub fn main() void {
    api.process(.{ .map = &.{}});
}
