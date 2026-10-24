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
fn DoThing(x: ZVal) void { _ = x; }
pub fn main() void {
    DoThing(.{ .int = 1 });
    DoThing(.{ .int = 2 });
}
