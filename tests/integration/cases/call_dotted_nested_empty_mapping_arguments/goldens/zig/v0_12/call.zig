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
const WorkerType_ = struct { fn process(self: WorkerType_, values: ZVal, count: ZVal) void { _ = self; _ = values; _ = count; } };
const ApiType_ = struct { worker: WorkerType_ = .{} };
const api: ApiType_ = .{};
pub fn main() void {
    api.worker.process(.{ .arr = &.{.{ .int = 1 }, .{ .map = &.{}}}}, .{ .int = 42 });
    api.worker.process(.{ .arr = &.{.{ .int = 2 }, .{ .map = &.{.{ .key = "x", .val = .{ .str = "s" } }}}}}, .{ .int = 43 });
}
