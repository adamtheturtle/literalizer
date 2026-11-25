const Http_ClientType_ = struct { fn fetch(self: Http_ClientType_, payload: anytype) void { _ = self; _ = payload; } };
const My_AppType_ = struct { http_client: Http_ClientType_ = .{} };
const my_app: My_AppType_ = .{};
pub fn main() void {
    my_app.http_client.fetch("hello");
    my_app.http_client.fetch(42);
    my_app.http_client.fetch(true);
}
