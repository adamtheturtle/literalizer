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
fn make_widget(before: ZVal, populated: ZVal, after: ZVal) ZVal { _ = before; _ = populated; _ = after; return .nil; }
pub fn main() void {
    _ = make_widget(.{ .arr = &.{}}, .{ .arr = &.{.{ .int = 1 }}}, .{ .arr = &.{}});
    _ = make_widget(.{ .arr = &.{.{ .str = "text" }}}, .{ .arr = &.{.{ .int = 2 }}}, .{ .arr = &.{}});
    _ = make_widget(.{ .arr = &.{}}, .{ .arr = &.{.{ .str = "text" }}}, .{ .arr = &.{}});
    _ = make_widget(.{ .arr = &.{.{ .str = "text" }}}, .{ .arr = &.{.{ .int = 2 }}}, .{ .arr = &.{.{ .int = 3 }}});
}
