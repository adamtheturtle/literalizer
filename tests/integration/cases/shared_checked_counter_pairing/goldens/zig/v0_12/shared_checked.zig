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
const std = @import("std");
var calls: usize = 0;
var checks: usize = 0;
const Counter = struct {
    fn accept(_: @This(), user: ZVal, timestamp: ZVal) bool {
        std.debug.assert(std.mem.eql(u8, user.str, if (calls == 0) "user_1" else "user_2"));
        std.debug.assert(timestamp.float == 100.0 + @as(f64, @floatFromInt(calls)));
        calls += 1;
        return std.mem.eql(u8, user.str, "user_1");
    }
};
fn checkResult(actual: bool, expected: ZVal) void {
    std.debug.assert(actual == expected.arr[0].bool);
    std.debug.assert(std.mem.eql(u8, expected.arr[1].str, if (checks == 0) "first" else "second"));
    checks += 1;
}
pub fn main() void {
    const counter = Counter{};
    checkResult(counter.accept(.{ .str = "user_1" }, .{ .float = 100.0 }), .{ .arr = &.{.{ .bool = true }, .{ .str = "first" }}});
    checkResult(counter.accept(.{ .str = "user_2" }, .{ .float = 101.0 }), .{ .arr = &.{.{ .bool = false }, .{ .str = "second" }}});
    std.debug.assert(calls == 2 and checks == 2);
}
