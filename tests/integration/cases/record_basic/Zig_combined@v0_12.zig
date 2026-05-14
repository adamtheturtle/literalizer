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
        .{ .key = "id", .val = .{ .int = 1 } },
        .{ .key = "description", .val = .{ .str = "She said \"hello\", then waved" } },
        .{ .key = "is_done", .val = .{ .bool = false } },
        .{ .key = "blocks", .val = .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }, .{ .int = 3 }}} },
    }};
    my_data = .{ .map = &.{
        .{ .key = "id", .val = .{ .int = 1 } },
        .{ .key = "description", .val = .{ .str = "She said \"hello\", then waved" } },
        .{ .key = "is_done", .val = .{ .bool = false } },
        .{ .key = "blocks", .val = .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }, .{ .int = 3 }}} },
    }};
    my_data = .nil;
}
