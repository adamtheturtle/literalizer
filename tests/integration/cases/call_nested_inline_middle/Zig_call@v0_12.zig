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
fn f(ops: ZVal) void { _ = ops; }
pub fn main() void {
    f(.{ .arr = &.{.{ .arr = &.{.{ .str = "DEL" }, .{ .str = "b" }, .{ .str = "10" }}}, .{ .arr = &.{.{ .str = "ADD" }, .{ .str = "a" }, .{ .str = "x" }}}}});  // note
    // next call
    f(.{ .arr = &.{.{ .arr = &.{.{ .str = "ADD" }, .{ .str = "c" }, .{ .str = "y" }}}}});
}
