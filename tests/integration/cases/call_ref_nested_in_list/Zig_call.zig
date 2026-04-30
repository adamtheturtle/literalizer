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
fn process(data: ZVal) void { _ = data; }
pub fn main() void {
    const my_var: ZVal = .{ .int = 42 };
    const my_other: ZVal = .{ .int = 7 };
    process(.{ .arr = &.{.{ .map = &.{.{ .key = "ref", .val = .{ .str = "my_var" } }}}, .{ .int = 42 }, .{ .str = "static" }}});
    process(.{ .arr = &.{.{ .map = &.{.{ .key = "ref", .val = .{ .str = "my_other" } }}}, .{ .int = 7 }, .{ .str = "label" }}});
}
