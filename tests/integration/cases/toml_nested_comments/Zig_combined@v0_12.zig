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
        // About the first dotted key.
        // About the second dotted key.
        .{ .key = "dotted", .val = .{ .map = &.{.{ .key = "first", .val = .{ .int = 1 } }, .{ .key = "second", .val = .{ .int = 2 } }}} },
        .{ .key = "plain", .val = .{ .int = 3 } },  // About the plain key.
        // Inside the table.
        .{ .key = "table", .val = .{ .map = &.{.{ .key = "inner", .val = .{ .int = 4 } }}} },
        // Before the first entry.
        // Before the second entry.
        .{ .key = "entries", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "name", .val = .{ .str = "one" } }}}, .{ .map = &.{.{ .key = "name", .val = .{ .str = "two" } }}}}} },
    }};
    my_data = .{ .map = &.{
        // About the first dotted key.
        // About the second dotted key.
        .{ .key = "dotted", .val = .{ .map = &.{.{ .key = "first", .val = .{ .int = 1 } }, .{ .key = "second", .val = .{ .int = 2 } }}} },
        .{ .key = "plain", .val = .{ .int = 3 } },  // About the plain key.
        // Inside the table.
        .{ .key = "table", .val = .{ .map = &.{.{ .key = "inner", .val = .{ .int = 4 } }}} },
        // Before the first entry.
        // Before the second entry.
        .{ .key = "entries", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "name", .val = .{ .str = "one" } }}}, .{ .map = &.{.{ .key = "name", .val = .{ .str = "two" } }}}}} },
    }};
    my_data = .nil;
}
