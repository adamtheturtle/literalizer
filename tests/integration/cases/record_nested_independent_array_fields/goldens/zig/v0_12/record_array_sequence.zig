const Record0 = struct { numbers: []const []const i64, words: []const []const []const u8 };
pub fn main() void {
    const my_data = Record0{
        .numbers = &.{
            &.{
                1,
            },
            &.{
                2,
            },
        },
        .words = &.{
            &.{
                "s",
            },
            &.{
                "t",
            },
        },
    };
    _ = my_data;
}
