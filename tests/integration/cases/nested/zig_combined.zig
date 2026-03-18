const ZVal = union(enum) {
    nil,
    bool: bool,
    int: i64,
    float: f64,
    str: []const u8,
    arr: []const ZVal,
    map: []const ZKV,
    set: []const ZVal,
};
const ZKV = struct { key: []const u8, val: ZVal };
pub fn main() void {
    {
        const my_data: ZVal = .{ .map = &.{
            .{ .key = "users", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "name", .val = .{ .str = "Bob" } }, .{ .key = "tags", .val = .{ .arr = &.{.{ .str = "admin" }, .{ .str = "user" }}} }}}, .{ .map = &.{.{ .key = "name", .val = .{ .str = "Carol" } }, .{ .key = "tags", .val = .{ .arr = &.{.{ .str = "guest" }}} }}}}} },
        }};
        _ = my_data;
    }
    var my_data: ZVal = undefined;
    my_data = .{ .map = &.{
        .{ .key = "users", .val = .{ .arr = &.{.{ .map = &.{.{ .key = "name", .val = .{ .str = "Bob" } }, .{ .key = "tags", .val = .{ .arr = &.{.{ .str = "admin" }, .{ .str = "user" }}} }}}, .{ .map = &.{.{ .key = "name", .val = .{ .str = "Carol" } }, .{ .key = "tags", .val = .{ .arr = &.{.{ .str = "guest" }}} }}}}} },
    }};
    const _my_data_read = my_data;
    _ = _my_data_read;
}
