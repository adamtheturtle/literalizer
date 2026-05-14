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
        .{ .key = "user", .val = .{ .map = &.{.{ .key = "id", .val = .{ .int = 1 } }, .{ .key = "name", .val = .{ .str = "Alice" } }}} },
        .{ .key = "project", .val = .{ .map = &.{.{ .key = "title", .val = .{ .str = "report" } }, .{ .key = "tags", .val = .{ .arr = &.{.{ .str = "draft" }, .{ .str = "urgent" }}} }}} },
    }};
    my_data = .{ .map = &.{
        .{ .key = "user", .val = .{ .map = &.{.{ .key = "id", .val = .{ .int = 1 } }, .{ .key = "name", .val = .{ .str = "Alice" } }}} },
        .{ .key = "project", .val = .{ .map = &.{.{ .key = "title", .val = .{ .str = "report" } }, .{ .key = "tags", .val = .{ .arr = &.{.{ .str = "draft" }, .{ .str = "urgent" }}} }}} },
    }};
    my_data = .nil;
}
