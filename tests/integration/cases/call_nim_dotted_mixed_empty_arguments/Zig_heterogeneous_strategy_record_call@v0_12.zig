const ThingType_ = struct { fn go(self: ThingType_, before: anytype, populated: anytype, after: anytype) i64 { _ = self; _ = before; _ = populated; _ = after; return 0; } };
const thing: ThingType_ = .{};
pub fn main() void {
    thing.go(&.{}, &.{1}, &.{});
    thing.go(&.{"text"}, &.{2}, &.{});
    thing.go(&.{}, &.{"text"}, &.{});
    thing.go(&.{"text"}, &.{2}, &.{3});
}
