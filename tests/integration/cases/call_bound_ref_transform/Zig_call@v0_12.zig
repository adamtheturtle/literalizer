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
fn f(a: ZVal) ZVal { _ = a; return .nil; }
fn repr(_arg: anytype) void { _ = _arg; }
pub fn main() void {
    const ref_data: ZVal = .{ .int = 1 };
    repr(f(ref_data));
}
