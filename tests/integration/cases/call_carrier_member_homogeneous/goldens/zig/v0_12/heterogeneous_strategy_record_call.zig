const AppType_ = struct { fn go(self: AppType_, first_value: anytype, second_value: anytype) void { _ = self; _ = first_value; _ = second_value; } };
const app: AppType_ = .{};
pub fn main() void {
    app.go(&.{1}, &.{2});
}
