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
        .{ .key = "i32_below", .val = .{ .int = -0o20000000001 } },
        .{ .key = "i32_minimum", .val = .{ .int = -0o20000000000 } },
        .{ .key = "i32_above", .val = .{ .int = -0o17777777777 } },
        .{ .key = "i32_maximum", .val = .{ .int = 0o17777777777 } },
        .{ .key = "i32_over", .val = .{ .int = 0o20000000000 } },
        .{ .key = "i64_minimum", .val = .{ .int = -0o1000000000000000000000 } },
        .{ .key = "i64_maximum", .val = .{ .int = 0o777777777777777777777 } },
    }};
    _ = my_data;
}
