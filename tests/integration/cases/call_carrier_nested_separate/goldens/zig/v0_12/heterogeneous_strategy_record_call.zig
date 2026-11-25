const ClientType_ = struct { fn go(self: ClientType_, first_value: anytype, second_value: anytype) void { _ = self; _ = first_value; _ = second_value; } };
const AppType_ = struct { client: ClientType_ = .{} };
const app: AppType_ = .{};
pub fn main() void {
    app.client.go(&.{1}, &.{"text"});
}
