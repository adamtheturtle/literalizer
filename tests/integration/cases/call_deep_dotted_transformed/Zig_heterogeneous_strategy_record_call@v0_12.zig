const ClientType_ = struct { fn fetch(self: ClientType_, payload: anytype) void { _ = self; _ = payload; } };
const AppType_ = struct { client: ClientType_ = .{} };
const app: AppType_ = .{};
fn emit(_arg: anytype) void { _ = _arg; }
pub fn main() void {
    emit(app.client.fetch("hello"));
    emit(app.client.fetch(42));
    emit(app.client.fetch(true));
}
