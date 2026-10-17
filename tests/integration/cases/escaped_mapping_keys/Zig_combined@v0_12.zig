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
        .{ .key = "quote\"backslash\\", .val = .{ .int = 1 } },
        .{ .key = "line\nbreak", .val = .{ .int = 2 } },
        .{ .key = "$(literal)${text}", .val = .{ .int = 3 } },
        .{ .key = "RStr prefix", .val = .{ .int = 4 } },
    }};
    my_data = .{ .map = &.{
        .{ .key = "quote\"backslash\\", .val = .{ .int = 1 } },
        .{ .key = "line\nbreak", .val = .{ .int = 2 } },
        .{ .key = "$(literal)${text}", .val = .{ .int = 3 } },
        .{ .key = "RStr prefix", .val = .{ .int = 4 } },
    }};
    my_data = .nil;
}
