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
        .{ .key = "title", .val = .{ .str = "report" } },
        .{ .key = "tags", .val = .{ .arr = &.{.{ .str = "draft" }, .{ .str = "urgent" }, .{ .str = "review" }}} },
        .{ .key = "priority", .val = .{ .int = 2 } },
    }};
    my_data = .{ .map = &.{
        .{ .key = "title", .val = .{ .str = "report" } },
        .{ .key = "tags", .val = .{ .arr = &.{.{ .str = "draft" }, .{ .str = "urgent" }, .{ .str = "review" }}} },
        .{ .key = "priority", .val = .{ .int = 2 } },
    }};
    my_data = .nil;
}
