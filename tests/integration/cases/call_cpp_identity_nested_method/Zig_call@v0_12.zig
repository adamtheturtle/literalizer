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
const ThingType_ = struct { fn go(self: ThingType_) void { _ = self; } };
const OuterType_ = struct { thing: ThingType_ = .{} };
const outer: OuterType_ = .{};
pub fn main() void {
    outer.thing.go();
}
