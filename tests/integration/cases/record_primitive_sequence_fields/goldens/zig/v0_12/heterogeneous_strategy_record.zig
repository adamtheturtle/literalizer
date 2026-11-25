const Record0 = struct { flags: []const bool, values: []const f64, ints: []const i64, text: []const []const u8, nested_flags: []const []const bool, nested_values: []const []const f64 };
pub fn main() void {
    const my_data = Record0{
        .flags = &.{
            true,
            false,
        },
        .values = &.{
            1.5,
            -2.25,
        },
        .ints = &.{
            1,
            2,
        },
        .text = &.{
            "a",
        },
        .nested_flags = &.{
            &.{
                true,
            },
            &.{
                false,
            },
        },
        .nested_values = &.{
            &.{
                1.5,
            },
            &.{
                2.25,
            },
        },
    };
    _ = my_data;
}
