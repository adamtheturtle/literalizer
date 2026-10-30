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
const FooType_ = struct { fn bar(self: FooType_, x: ZVal) void { _ = self; _ = x; } };
const FooType_ = struct { Foo: FooType_ = .{} };
const AType_ = struct { foo: FooType_ = .{} };
const a: AType_ = .{};
pub fn main() void {
    a.foo.Foo.bar(.{ .arr = &.{.{ .int = 1 }}});
}
