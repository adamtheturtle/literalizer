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
fn emit(_arg: anytype) void { _ = _arg; }
pub fn main() void {
    emit(app.client.fetch(.{ .str = "hello" }));
    emit(app.client.fetch(.{ .int = 42 }));
    emit(app.client.fetch(.{ .bool = true }));
}
