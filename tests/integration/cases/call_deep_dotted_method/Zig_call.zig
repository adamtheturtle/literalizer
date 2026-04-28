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
const ClientType_ = struct { fn post(self: ClientType_, data: ZVal) void { _ = self; _ = data; } };
const ApiType_ = struct { client: ClientType_ = .{} };
const ObjType_ = struct { api: ApiType_ = .{} };
const obj: ObjType_ = .{};
pub fn main() void {
    obj.api.client.post(.{ .str = "hello" });
    obj.api.client.post(.{ .int = 42 });
    obj.api.client.post(.{ .bool = true });
}
