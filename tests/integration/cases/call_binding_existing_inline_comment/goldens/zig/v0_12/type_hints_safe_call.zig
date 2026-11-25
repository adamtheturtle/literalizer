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
    const expected = [_]i64{2, 42, 1, 42, 2, 142};
    if (event_index >= 6 or actual != expected[event_index]) @panic("receiver event changed");
    event_index += 1;
}
fn make_widget(count: ZVal) ZVal { observe_event(1); observe_event(count.int); return .{ .int = count.int + 100 }; }
fn consume_widget(count: ZVal) void { observe_event(2); observe_event(count.int); }
fn verify_events() void { if (event_index != 6) @panic("missing receiver events"); }
pub fn main() void {
    var my_data: ZVal = .{ .int = 42 };
    consume_widget(my_data);
    my_data = make_widget(.{ .int = 42 }); // note
    consume_widget(my_data);
    verify_events();
    _ = &my_data;
}
