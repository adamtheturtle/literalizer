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
    const expected = [_]i64{1, 42, 2, 142};
    if (event_index >= 4 or actual != expected[event_index]) @panic("receiver event changed");
    event_index += 1;
}
fn process(value: ZVal) ZVal { observe_event(1); observe_event(value.int); return .{ .int = value.int + 100 }; }
fn emit(value: ZVal) void { observe_event(2); observe_event(value.int); }
fn verify_events() void { if (event_index != 4) @panic("missing receiver events"); }
pub fn main() void {
    emit(process(.{ .int = 42 }));
    verify_events();
}
