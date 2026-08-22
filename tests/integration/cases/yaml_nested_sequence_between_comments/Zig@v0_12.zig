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
    const my_data: ZVal = .{ .arr = &.{
        .{ .arr = &.{
            .{ .map = &.{.{ .key = "item", .val = .{ .str = "existing" } }}},
            .{ .str = "kept" },
            // This comment trails the first pair.
        }},
        .{ .arr = &.{.{ .map = &.{.{ .key = "item", .val = .{ .str = "next" } }}}, .{ .str = "also kept" }}},
        // This comment describes the last pair.
        .{ .arr = &.{.{ .map = &.{.{ .key = "item", .val = .{ .str = "last" } }}}, .{ .str = "kept too" }}},
    }};
    _ = my_data;
}
