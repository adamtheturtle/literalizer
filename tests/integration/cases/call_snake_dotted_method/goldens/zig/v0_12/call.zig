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
const Http_ClientType_ = struct { fn fetch(self: Http_ClientType_, payload: ZVal) void { _ = self; _ = payload; } };
const My_AppType_ = struct { http_client: Http_ClientType_ = .{} };
const my_app: My_AppType_ = .{};
pub fn main() void {
    my_app.http_client.fetch(.{ .str = "hello" });
    my_app.http_client.fetch(.{ .int = 42 });
    my_app.http_client.fetch(.{ .bool = true });
}
