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
pub fn main() void {
    var my_data: ZVal = .{ .arr = &.{
        .{ .map = &.{.{ .key = "call", .val = .{ .str = "send" } }, .{ .key = "args", .val = .{ .arr = &.{.{ .int = 1 }, .{ .str = "email" }, .{ .str = "a@gmail.com" }, .{ .int = 100 }}} }}},
        .{ .map = &.{.{ .key = "call", .val = .{ .str = "recv" } }, .{ .key = "args", .val = .{ .arr = &.{.{ .int = 2 }, .{ .str = "sms" }, .{ .str = "b@example.com" }, .{ .int = 200 }}} }}},
    }};
    my_data = .{ .arr = &.{
        .{ .map = &.{.{ .key = "call", .val = .{ .str = "send" } }, .{ .key = "args", .val = .{ .arr = &.{.{ .int = 1 }, .{ .str = "email" }, .{ .str = "a@gmail.com" }, .{ .int = 100 }}} }}},
        .{ .map = &.{.{ .key = "call", .val = .{ .str = "recv" } }, .{ .key = "args", .val = .{ .arr = &.{.{ .int = 2 }, .{ .str = "sms" }, .{ .str = "b@example.com" }, .{ .int = 200 }}} }}},
    }};
    my_data = .nil;
}
