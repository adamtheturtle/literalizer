const ClientType_ = struct { fn fetch(self: ClientType_, payload: anytype) void { _ = self; _ = payload; } };
const AppType_ = struct { client: ClientType_ = .{} };
const app: AppType_ = .{};
pub fn main() void {
    app.client.fetch("hello");
    app.client.fetch(42);
    app.client.fetch(true);
}
