const Record1 = struct { numbers: []const i64, strings: []const []const u8 };
const Record0 = struct { omap_value: []const struct { key: []const u8, val: i64 }, sibling_lists: Record1, ref_marker_present: []const []const u8 };
pub fn main() void {
    const my_data = Record0{
        .omap_value = &.{
            .{ .key = "first", .val = 1 },
        },
        .sibling_lists = Record1{
            .numbers = &.{
                1,
                2,
            },
            .strings = &.{
                "x",
                "y",
            },
        },
        .ref_marker_present = &.{
            "$keep",
            "z",
        },
    };
    _ = my_data;
}
