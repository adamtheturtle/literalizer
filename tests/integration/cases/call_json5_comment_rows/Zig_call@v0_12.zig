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
fn f(a: ZVal, b: ZVal) void { _ = a; _ = b; }
pub fn main() void {
    // calls heading
    // before call one
    // first argument
    f(.{ .int = 1 }, .{ .int = 2 });  // after call one
    // second argument
    f(.{ .int = 3 }, .{ .int = 4 });
    // after all calls
}
