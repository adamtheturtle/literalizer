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
const AppType_ = struct { fn go(self: AppType_, first_value: ZVal, second_value: ZVal) void { _ = self; _ = first_value; _ = second_value; } };
const app: AppType_ = .{};
pub fn main() void {
    app.go(.{ .arr = &.{.{ .int = 1 }}}, .{ .arr = &.{.{ .int = 2 }}});
}
