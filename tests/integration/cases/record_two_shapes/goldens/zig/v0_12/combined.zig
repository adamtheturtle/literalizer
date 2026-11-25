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
    var my_data: ZVal = .{ .map = &.{
        .{ .key = "metrics", .val = .{ .map = &.{.{ .key = "count", .val = .{ .int = 100 } }, .{ .key = "rate", .val = .{ .int = 50 } }}} },
        .{ .key = "flags", .val = .{ .map = &.{.{ .key = "retries", .val = .{ .int = 3 } }, .{ .key = "timeout", .val = .{ .int = 30 } }}} },
    }};
    my_data = .{ .map = &.{
        .{ .key = "metrics", .val = .{ .map = &.{.{ .key = "count", .val = .{ .int = 100 } }, .{ .key = "rate", .val = .{ .int = 50 } }}} },
        .{ .key = "flags", .val = .{ .map = &.{.{ .key = "retries", .val = .{ .int = 3 } }, .{ .key = "timeout", .val = .{ .int = 30 } }}} },
    }};
    my_data = .nil;
}
