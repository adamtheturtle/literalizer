const @"record value" = union(enum) {
    nil,
    bool: bool,
    int: i64,
    uint: u64,
    float: f64,
    str: []const u8,
    arr: []const @"record value",
    map: []const @"record entry",
    set: []const @"record value",
};
const @"record entry" = struct { key: []const u8, val: @"record value" };
const Record0 = struct { input: @"record value", expected: @"record value" };
pub fn main() void {
    const my_data = &.{
        Record0{ .input = .{ .map = &.{.{ .key = "kind", .val = .{ .str = "add" } }, .{ .key = "item_id", .val = .{ .str = "item_1" } }, .{ .key = "urgent", .val = .{ .bool = true } }}}, .expected = .{ .map = &.{.{ .key = "item_id", .val = .{ .str = "item_1" } }, .{ .key = "state", .val = .{ .str = "pending" } }}} },
        Record0{ .input = .{ .map = &.{.{ .key = "kind", .val = .{ .str = "remove" } }, .{ .key = "item_id", .val = .{ .str = "item_9" } }}}, .expected = .{ .map = &.{.{ .key = "error", .val = .{ .str = "not_found" } }}} },
    };
    _ = my_data;
}
