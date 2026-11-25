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
const ProcessType_ = struct { fn fetch(self: ProcessType_, data: ZVal) void { _ = self; _ = data; } };
const AppType_ = struct { process: ProcessType_ = .{} };
const app: AppType_ = .{};
pub fn main() void {
    app.process.fetch(.{ .map = &.{.{ .key = "data", .val = .{ .str = "hello" } }}});
    app.process.fetch(.{ .map = &.{.{ .key = "data", .val = .{ .int = 42 } }}});
    app.process.fetch(.{ .map = &.{.{ .key = "data", .val = .{ .bool = true } }}});
}
