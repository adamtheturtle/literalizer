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
const ClientType_ = struct { fn go(self: ClientType_, first_value: ZVal, second_value: ZVal) void { _ = self; _ = first_value; _ = second_value; } };
const AppType_ = struct { client: ClientType_ = .{} };
const app: AppType_ = .{};
pub fn main() void {
    app.client.go(.{ .arr = &.{.{ .int = 1 }}}, .{ .arr = &.{.{ .str = "text" }}});
}
