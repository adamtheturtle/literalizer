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
        .{ .key = "user_name", .val = .{ .int = 1 } },
        .{ .key = "user.name", .val = .{ .int = 2 } },
        .{ .key = "user-name", .val = .{ .int = 3 } },
        .{ .key = "field_name_that_is_really_quite_long_one", .val = .{ .int = 4 } },
        .{ .key = "field_name_that_is_really_quite_long_two", .val = .{ .int = 5 } },
    }};
    _ = my_data;
}
