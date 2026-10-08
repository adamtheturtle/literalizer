const Record0 = struct { a: []const []const i64, b: []const []const i64 };
pub fn main() void {
    const my_data = Record0{
        .a = &.{
            &.{
                1,
                2,
            },
            &.{
                3,
            },
        },
        .b = &.{
            &.{},
            &.{
                1,
            },
        },
    };
    _ = my_data;
}
