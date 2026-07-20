fn process(value: anytype) void { _ = value; }
pub fn main() void {
    process(.{ .map = &.{.{ .key = "value", .val = 1 }}});
    process(.{ .map = &.{.{ .key = "value", .val = "hello" }}});
}
