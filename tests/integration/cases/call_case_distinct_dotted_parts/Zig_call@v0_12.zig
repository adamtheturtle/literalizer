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
const FooType_2 = struct { fn bar(self: FooType_2, x: ZVal) void { _ = self; _ = x; } };
const FooType_1 = struct { Foo: FooType_2 = .{} };
const AType_ = struct { foo: FooType_1 = .{} };
const a: AType_ = .{};
pub fn main() void {
    a.foo.Foo.bar(.{ .arr = &.{.{ .int = 1 }}});
}
