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
        // before
        .{ .key = "answer", .val = .{ .int = 42 } },  // inline
        .{ .key = "plain", .val = .{ .str = "ok" } },
        // trailing
    }};
    my_data = .{ .map = &.{
        // before
        .{ .key = "answer", .val = .{ .int = 42 } },  // inline
        .{ .key = "plain", .val = .{ .str = "ok" } },
        // trailing
    }};
    my_data = .nil;
}
