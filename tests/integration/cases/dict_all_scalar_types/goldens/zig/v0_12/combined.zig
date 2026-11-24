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
        .{ .key = "s", .val = .{ .str = "string" } },
        .{ .key = "i", .val = .{ .int = 1 } },
        .{ .key = "f", .val = .{ .float = 1.5 } },
        .{ .key = "b", .val = .{ .bool = true } },
        .{ .key = "n", .val = .nil },
        .{ .key = "d", .val = .{ .int = 1705276800 } },
        .{ .key = "dt", .val = .{ .int = 1705320000 } },
        .{ .key = "by", .val = .{ .str = "48656c6c6f" } },
    }};
    my_data = .{ .map = &.{
        .{ .key = "s", .val = .{ .str = "string" } },
        .{ .key = "i", .val = .{ .int = 1 } },
        .{ .key = "f", .val = .{ .float = 1.5 } },
        .{ .key = "b", .val = .{ .bool = true } },
        .{ .key = "n", .val = .nil },
        .{ .key = "d", .val = .{ .int = 1705276800 } },
        .{ .key = "dt", .val = .{ .int = 1705320000 } },
        .{ .key = "by", .val = .{ .str = "48656c6c6f" } },
    }};
    my_data = .nil;
}
