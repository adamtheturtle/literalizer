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
const ThingType_ = struct { fn go(self: ThingType_, before: ZVal, populated: ZVal, after: ZVal) ZVal { _ = self; _ = before; _ = populated; _ = after; return .nil; } };
const thing: ThingType_ = .{};
pub fn main() void {
    thing.go(.{ .arr = &.{}}, .{ .arr = &.{.{ .int = 1 }}}, .{ .arr = &.{}});
    thing.go(.{ .arr = &.{.{ .str = "text" }}}, .{ .arr = &.{.{ .int = 2 }}}, .{ .arr = &.{}});
    thing.go(.{ .arr = &.{}}, .{ .arr = &.{.{ .str = "text" }}}, .{ .arr = &.{}});
    thing.go(.{ .arr = &.{.{ .str = "text" }}}, .{ .arr = &.{.{ .int = 2 }}}, .{ .arr = &.{.{ .int = 3 }}});
}
