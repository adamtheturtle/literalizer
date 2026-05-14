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
    process(.{ .map = &.{.{ .key = "type", .val = .{ .str = "create" } }, .{ .key = "pr_id", .val = .{ .str = "pr_1" } }}});  // first case
    process(.{ .map = &.{.{ .key = "type", .val = .{ .str = "update" } }, .{ .key = "pr_id", .val = .{ .str = "pr_2" } }}});  // second case
    // third case
    process(.{ .map = &.{.{ .key = "type", .val = .{ .str = "delete" } }, .{ .key = "pr_id", .val = .{ .str = "pr_3" } }}});
}
