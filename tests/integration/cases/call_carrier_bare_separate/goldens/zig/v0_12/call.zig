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
fn make_widget(first_value: ZVal, second_value: ZVal) void { _ = first_value; _ = second_value; }
pub fn main() void {
    make_widget(.{ .arr = &.{.{ .int = 1 }}}, .{ .arr = &.{.{ .str = "text" }}});
}
