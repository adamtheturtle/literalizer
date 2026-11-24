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
var event_index: usize = 0;
fn observe_event(actual: i64) void {
    const expected = [_]i64{1, 42};
    if (event_index >= 2 or actual != expected[event_index]) @panic("receiver event changed");
    event_index += 1;
}
fn f(a: ZVal) void { observe_event(1); observe_event(a.int); }
fn verify_events() void { if (event_index != 2) @panic("missing receiver events"); }
pub fn main() void {
    // scalar heading
    // second heading line
    // scalar inline
    // inline continuation
    // scalar trailing
    f(.{ .int = 42 });
    verify_events();
}
