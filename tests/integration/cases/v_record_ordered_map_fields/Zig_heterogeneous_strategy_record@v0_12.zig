const Record0 = struct { numbers: []const struct { key: []const u8, val: i64 }, words: []const struct { key: []const u8, val: []const u8 }, nested: []const struct { key: []const u8, val: []const i64 }, empty: []const struct { key: []const u8, val: i64 }, flag: bool, nested_maps: []const struct { key: []const u8, val: []const struct { key: []const u8, val: i64 } }, empty_nested_maps: []const struct { key: []const u8, val: []const struct { key: []const u8, val: i64 } } };
pub fn main() void {
    const my_data = Record0{
        .numbers = &.{
            .{ .key = "first", .val = 1 },
        },
        .words = &.{
            .{ .key = "first", .val = "s" },
        },
        .nested = &.{
            .{ .key = "first", .val = &.{
                1,
                2,
            } },
        },
        .empty = .{},
        .flag = true,
        .nested_maps = &.{
            .{ .key = "first", .val = &.{
                .{ .key = "nested", .val = 1 },
            } },
        },
        .empty_nested_maps = &.{
            .{ .key = "first", .val = .{} },
        },
    };
    _ = my_data;
}
