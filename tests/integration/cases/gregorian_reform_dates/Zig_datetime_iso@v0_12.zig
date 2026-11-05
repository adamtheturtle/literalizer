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
        .{ .key = "ancient_date", .val = .{ .int = -14826672000 } },
        .{ .key = "modern_date", .val = .{ .int = 1705276800 } },
        .{ .key = "before_date", .val = .{ .int = -12220243200 } },
        .{ .key = "gap_date", .val = .{ .int = -12219724800 } },
        .{ .key = "transition_date", .val = .{ .int = -12219292800 } },
        .{ .key = "after_date", .val = .{ .int = -12219206400 } },
        .{ .key = "before_naive", .val = .{ .str = "1582-10-04T12:30:00.000001" } },
        .{ .key = "gap_naive", .val = .{ .str = "1582-10-10T12:30:00.500000" } },
        .{ .key = "transition_positive", .val = .{ .str = "1582-10-15T00:30:00+18:00" } },
        .{ .key = "transition_negative", .val = .{ .str = "1582-10-15T23:30:00-18:00" } },
        .{ .key = "after_positive", .val = .{ .str = "1582-10-16T00:30:00+18:00" } },
    }};
    _ = my_data;
}
