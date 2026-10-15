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
fn process(value: ZVal) ZVal { _ = value; return .nil; }
pub fn main() void {
    process(.{ .str = "time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)" });
}
