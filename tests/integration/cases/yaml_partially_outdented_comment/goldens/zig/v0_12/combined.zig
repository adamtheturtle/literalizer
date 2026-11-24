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
        .{ .key = "a", .val = .{ .map = &.{
            .{ .key = "b", .val = .{ .arr = &.{.{ .int = 1 }}} },
            // Outdented from the sequence, so the inner mapping claims this.
            .{ .key = "c", .val = .{ .int = 2 } },
        }} },
        // Outdented from the inner mapping too, so the root claims this.
        .{ .key = "d", .val = .{ .int = 3 } },
    }};
    my_data = .{ .map = &.{
        .{ .key = "a", .val = .{ .map = &.{
            .{ .key = "b", .val = .{ .arr = &.{.{ .int = 1 }}} },
            // Outdented from the sequence, so the inner mapping claims this.
            .{ .key = "c", .val = .{ .int = 2 } },
        }} },
        // Outdented from the inner mapping too, so the root claims this.
        .{ .key = "d", .val = .{ .int = 3 } },
    }};
    my_data = .nil;
}
