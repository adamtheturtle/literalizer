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
        .{ .key = "i32_below", .val = .{ .int = -2_147_483_649 } },
        .{ .key = "i32_minimum", .val = .{ .int = -2_147_483_648 } },
        .{ .key = "i32_above", .val = .{ .int = -2_147_483_647 } },
        .{ .key = "i32_maximum", .val = .{ .int = 2_147_483_647 } },
        .{ .key = "i32_over", .val = .{ .int = 2_147_483_648 } },
        .{ .key = "i64_minimum", .val = .{ .int = -9_223_372_036_854_775_808 } },
        .{ .key = "i64_maximum", .val = .{ .int = 9_223_372_036_854_775_807 } },
    }};
    _ = my_data;
}
