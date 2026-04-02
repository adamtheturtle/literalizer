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
    var my_data: ZVal = .{ .map = &.{
        .{ .key = "1", .val = .{ .str = "one" } },
        .{ .key = "2", .val = .{ .str = "two" } },
        .{ .key = "42", .val = .{ .str = "answer" } },
    }};
    my_data = .{ .map = &.{
        .{ .key = "1", .val = .{ .str = "one" } },
        .{ .key = "2", .val = .{ .str = "two" } },
        .{ .key = "42", .val = .{ .str = "answer" } },
    }};
    my_data = .nil;
}
