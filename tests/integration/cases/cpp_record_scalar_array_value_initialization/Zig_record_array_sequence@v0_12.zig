const Record0 = struct { numbers: []const i64, nested_numbers: []const []const i64, words: []const []const u8, flag: bool };
pub fn main() void {
    const my_data = Record0{
        .numbers = &.{
            1,
            2,
        },
        .nested_numbers = &.{
            &.{
                3,
                4,
            },
            &.{
                5,
                6,
            },
        },
        .words = &.{
            "s",
        },
        .flag = true,
    };
    _ = my_data;
}
