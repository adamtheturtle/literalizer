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
const FooType_1 = struct { fn bar(self: FooType_1, x: ZVal) void { _ = self; _ = x; } };
const FooType_0 = struct { Foo: FooType_1 = .{} };
const foo: FooType_0 = .{};
pub fn main() void {
    foo.Foo.bar(.{ .arr = &.{.{ .int = 1 }}});
}
