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
        .{ .key = "omap_value", .val = .{ .map = &.{.{ .key = "first", .val = .{ .int = 1 } }}} },
        .{ .key = "sibling_lists", .val = .{ .map = &.{.{ .key = "numbers", .val = .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }}} }, .{ .key = "strings", .val = .{ .arr = &.{.{ .str = "x" }, .{ .str = "y" }}} }}} },
        .{ .key = "ref_marker_present", .val = .{ .arr = &.{.{ .str = "$keep" }, .{ .str = "z" }}} },
    }};
    my_data = .{ .map = &.{
        .{ .key = "omap_value", .val = .{ .map = &.{.{ .key = "first", .val = .{ .int = 1 } }}} },
        .{ .key = "sibling_lists", .val = .{ .map = &.{.{ .key = "numbers", .val = .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }}} }, .{ .key = "strings", .val = .{ .arr = &.{.{ .str = "x" }, .{ .str = "y" }}} }}} },
        .{ .key = "ref_marker_present", .val = .{ .arr = &.{.{ .str = "$keep" }, .{ .str = "z" }}} },
    }};
    my_data = .nil;
}
