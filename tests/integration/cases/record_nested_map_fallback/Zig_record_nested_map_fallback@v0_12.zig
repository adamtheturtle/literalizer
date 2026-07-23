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
const Record0 = struct { name: []const u8, input: ZVal, expected: ZVal };
pub fn main() void {
    const my_data = &.{
        Record0{ .name = "test_1", .input = .{ .map = &.{.{ .key = "type", .val = .{ .str = "create" } }, .{ .key = "pr_id", .val = .{ .str = "pr_1" } }, .{ .key = "draft", .val = .{ .bool = true } }, .{ .key = "missing", .val = .nil }}}, .expected = .{ .map = &.{.{ .key = "pr_id", .val = .{ .str = "pr_1" } }, .{ .key = "status", .val = .{ .str = "draft" } }}} },
        Record0{ .name = "test_2", .input = .{ .map = &.{.{ .key = "type", .val = .{ .str = "publish" } }, .{ .key = "pr_id", .val = .{ .str = "pr_1" } }}}, .expected = .{ .map = &.{.{ .key = "error", .val = .{ .str = "invalid_operation" } }}} },
    };
    _ = my_data;
}
