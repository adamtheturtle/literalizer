const Record0 = struct { numbers: []const i64, words: []const []const u8 };
pub fn main() void {
    const my_data = Record0{
        .numbers = &.{
            1,
        },
        .words = &.{
            "s",
        },
    };
    _ = my_data;
}
