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
fn process(value: ZVal) void { _ = value; }
pub fn main() void {
    // Test cases
    process(.{ .str = "hello" });  // single word
    process(.{ .str = "hello world" });  // two words
    // trailing comment
}
