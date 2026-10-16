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
fn f(a: ZVal) void { _ = a; }
pub fn main() void {
    // scalar heading
    // second heading line
    // scalar inline
    // inline continuation
    // scalar trailing
    f(.{ .int = 42 });
}
