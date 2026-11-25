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
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "below", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .int = 1 }}}}}}}}}}}}}}}}} },
        .{ .key = "boundary", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .int = 2 }}}}}}}}}}}}}}}}}}} },
        .{ .key = "multiple", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .int = 3 }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}} },
        .{ .key = "text", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .str = "value" }}}}}}}}}}}}}}}}}}} },
        .{ .key = "boolean", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .bool = true }}}}}}}}}}}}}}}}}}} },
        .{ .key = "float", .val = .{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .arr = &.{.{ .float = 1.5 }}}}}}}}}}}}}}}}}}} },
    }};
    _ = my_data;
}
