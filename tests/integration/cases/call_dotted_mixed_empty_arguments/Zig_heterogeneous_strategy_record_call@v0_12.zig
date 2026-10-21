const ThingType_ = struct { fn go(self: ThingType_, before: anytype, populated: anytype, after: anytype) i64 { _ = self; _ = before; _ = populated; _ = after; return 0; } };
const thing: ThingType_ = .{};
pub fn main() void {
    _ = thing.go(&.{}, &.{1}, &.{});
    _ = thing.go(&.{"text"}, &.{2}, &.{});
    _ = thing.go(&.{}, &.{"text"}, &.{});
    _ = thing.go(&.{"text"}, &.{2}, &.{3});
}
