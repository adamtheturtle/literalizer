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
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 100 } }, .{ .key = "label", .val = .{ .str = "first item" } }, .{ .key = "enabled", .val = .{ .bool = false } }, .{ .key = "related_ids", .val = .{ .arr = &.{.{ .int = 102 }, .{ .int = 103 }}} }}},
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 101 } }, .{ .key = "label", .val = .{ .str = "second item" } }, .{ .key = "enabled", .val = .{ .bool = true } }, .{ .key = "related_ids", .val = .{ .arr = &.{.{ .int = 100 }}} }}},
    }};
    my_data = .{ .arr = &.{
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 100 } }, .{ .key = "label", .val = .{ .str = "first item" } }, .{ .key = "enabled", .val = .{ .bool = false } }, .{ .key = "related_ids", .val = .{ .arr = &.{.{ .int = 102 }, .{ .int = 103 }}} }}},
        .{ .map = &.{.{ .key = "id", .val = .{ .int = 101 } }, .{ .key = "label", .val = .{ .str = "second item" } }, .{ .key = "enabled", .val = .{ .bool = true } }, .{ .key = "related_ids", .val = .{ .arr = &.{.{ .int = 100 }}} }}},
    }};
    my_data = .nil;
}
