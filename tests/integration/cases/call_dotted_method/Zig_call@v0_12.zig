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
const ClientType_ = struct { fn fetch(self: ClientType_, payload: ZVal) void { _ = self; _ = payload; } };
const AppType_ = struct { client: ClientType_ = .{} };
const app: AppType_ = .{};
pub fn main() void {
    app.client.fetch(.{ .str = "hello" });
    app.client.fetch(.{ .int = 42 });
    app.client.fetch(.{ .bool = true });
}
