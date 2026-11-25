const ThingType_ = struct { fn go(self: ThingType_, value: anytype) i64 { _ = self; _ = value; return 0; } };
const thing: ThingType_ = .{};
pub fn main() void {
    const my_data = thing.go(&.{1});
    _ = my_data;
}
