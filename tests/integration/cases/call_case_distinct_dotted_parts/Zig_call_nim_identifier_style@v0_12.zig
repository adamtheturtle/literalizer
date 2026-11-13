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
const FoobarType_ = struct { fn bar(self: FoobarType_, x: ZVal) void { _ = self; _ = x; } };
const Foo_BarType_ = struct { fooBar: FoobarType_ = .{} };
const AType_ = struct { foo_bar: Foo_BarType_ = .{} };
const a: AType_ = .{};
pub fn main() void {
    a.foo_bar.fooBar.bar(.{ .arr = &.{.{ .int = 1 }}});
}
