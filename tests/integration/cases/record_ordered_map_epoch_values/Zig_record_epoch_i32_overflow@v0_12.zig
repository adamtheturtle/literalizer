const Record0 = struct { values: []const struct { key: []const u8, val: i64 }, flag: bool, nested_values: []const struct { key: []const u8, val: []const struct { key: []const u8, val: i64 } }, list_values: []const struct { key: []const u8, val: []const i64 } };
pub fn main() void {
    const my_data = Record0{
        .values = &.{
            .{ .key = "first", .val = 2208988800 },
        },
        .flag = true,
        .nested_values = &.{
            .{ .key = "first", .val = &.{
                .{ .key = "nested", .val = 2208988800 },
            } },
        },
        .list_values = &.{
            .{ .key = "first", .val = &.{
                2208988800,
            } },
        },
    };
    _ = my_data;
}
