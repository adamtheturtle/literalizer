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
const @"literalizer call value" = ZVal;
const ObjType_ = struct { fn ZVal(self: ObjType_, value: @"literalizer call value") void { _ = self; _ = value; } };
const obj: ObjType_ = .{};
pub fn main() void {
    obj.ZVal(.{ .int = 1 });
}
