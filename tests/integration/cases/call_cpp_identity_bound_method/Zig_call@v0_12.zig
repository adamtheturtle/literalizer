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
const ThingType_ = struct { fn go(self: ThingType_, value: ZVal) void { _ = self; _ = value; } };
const thing: ThingType_ = .{};
pub fn main() void {
    const item: ZVal = .{ .arr = &.{
        .{ .int = 1 },
        .{ .int = 2 },
    }};
    thing.go(item);
}
