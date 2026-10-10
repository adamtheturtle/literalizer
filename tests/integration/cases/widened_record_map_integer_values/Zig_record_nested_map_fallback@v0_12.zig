const @"literalizer record value" = union(enum) {
    nil,
    bool: bool,
    int: i64,
    uint: u64,
    float: f64,
    str: []const u8,
    arr: []const @"literalizer record value",
    map: []const @"literalizer record entry",
    set: []const @"literalizer record value",
};
const @"literalizer record entry" = struct { key: []const u8, val: @"literalizer record value" };
const Record0 = struct { input: @"literalizer record value" };
pub fn main() void {
    const my_data = &.{
        Record0{ .input = .{ .map = &.{.{ .key = "a", .val = .{ .int = 1 } }}} },
        Record0{ .input = .{ .map = &.{.{ .key = "b", .val = .{ .int = 2 } }}} },
    };
    _ = my_data;
}
