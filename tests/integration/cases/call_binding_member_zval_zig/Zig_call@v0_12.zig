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
const @"call value" = ZVal;
const ObjType_ = struct { fn ZVal(self: ObjType_, _arg: anytype) @"call value" { _ = self; _ = _arg; return .nil; } };
const obj: ObjType_ = .{};
pub fn main() void {
    const my_data = obj.ZVal(.{ .int = 42 }); // note
    _ = my_data;
}
