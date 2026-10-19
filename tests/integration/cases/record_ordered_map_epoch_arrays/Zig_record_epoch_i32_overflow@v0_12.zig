const Record0 = struct { values: *const struct { struct { key: []const u8, val: []const []const i64 }, struct { key: []const u8, val: []const []const i64 }, struct { key: []const u8, val: []const []const i64 }, struct { key: []const u8, val: []const []const i64 }, struct { key: []const u8, val: []const []const i64 }, struct { key: []const u8, val: []const u8 } }, flag: bool, direct_arrays: []const []const i64 };
pub fn main() void {
    const my_data = Record0{
        .values = &.{
            .{ .key = "wide", .val = &.{
                &.{
                    2208988800,
                },
                &.{},
            } },
            .{ .key = "narrow", .val = &.{
                &.{
                    946684800,
                },
            } },
            .{ .key = "negative", .val = &.{
                &.{
                    -2208988800,
                },
            } },
            .{ .key = "shifted", .val = &.{
                &.{
                    2208988800,
                },
            } },
            .{ .key = "mixed_width", .val = &.{
                &.{
                    946684800,
                },
                &.{
                    2208988800,
                },
            } },
            .{ .key = "text", .val = "preserve" },
        },
        .flag = true,
        .direct_arrays = &.{
            &.{
                2208988800,
            },
            &.{},
        },
    };
    _ = my_data;
}
