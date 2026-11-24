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
const MgrType_ = struct { fn run(self: MgrType_, operation: ZVal) void { _ = self; _ = operation; } };
const AppType_ = struct { mgr: MgrType_ = .{} };
const app: AppType_ = .{};
pub fn main() void {
    app.mgr.run(.{ .map = &.{.{ .key = "type", .val = .{ .str = "create" } }, .{ .key = "pr_id", .val = .{ .str = "pr_1" } }, .{ .key = "draft", .val = .{ .bool = true } }}});
    app.mgr.run(.{ .map = &.{.{ .key = "type", .val = .{ .str = "create" } }, .{ .key = "pr_id", .val = .{ .str = "pr_2" } }}});
}
