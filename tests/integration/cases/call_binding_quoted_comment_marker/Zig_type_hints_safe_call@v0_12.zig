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
fn make_widget(text: ZVal) void { _ = text; }
pub fn main() void {
    const my_data = make_widget(.{ .str = "first \"quote\"\n// string body" }); // note
    // extra
    _ = my_data;
}
