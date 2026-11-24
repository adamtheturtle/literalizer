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
const ObjType_ = struct { fn ZKV(self: ObjType_, value: ZVal) void { _ = self; _ = value; } };
const obj: ObjType_ = .{};
pub fn main() void {
    obj.ZKV(.{ .int = 1 });
}
