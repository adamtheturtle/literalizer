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
const ClassType_ = struct { fn member(self: ClassType_, a: ZVal) void { _ = self; _ = a; } };
const class: ClassType_ = .{};
pub fn main() void {
    class.member(.{ .int = 42 });
}
