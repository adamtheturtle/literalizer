const ClientType_ = struct { fn post(self: ClientType_, data: anytype) void { _ = self; _ = data; } };
const ApiType_ = struct { client: ClientType_ = .{} };
const ObjType_ = struct { api: ApiType_ = .{} };
const obj: ObjType_ = .{};
pub fn main() void {
    obj.api.client.post("hello");
    obj.api.client.post(42);
    obj.api.client.post(true);
}
