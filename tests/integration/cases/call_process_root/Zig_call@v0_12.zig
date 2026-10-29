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
const ApiType_ = struct { fn fetch(self: ApiType_, data: ZVal) void { _ = self; _ = data; } };
const ProcessType_ = struct { api: ApiType_ = .{} };
const process: ProcessType_ = .{};
pub fn main() void {
    process.api.fetch(.{ .map = &.{.{ .key = "data", .val = .{ .str = "hello" } }}});
    process.api.fetch(.{ .map = &.{.{ .key = "data", .val = .{ .int = 42 } }}});
    process.api.fetch(.{ .map = &.{.{ .key = "data", .val = .{ .bool = true } }}});
}
