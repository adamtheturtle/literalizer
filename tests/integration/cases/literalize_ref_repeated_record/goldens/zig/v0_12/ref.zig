const Record0 = struct { value: []const i64 };
pub fn main() void {
    const shared = Record0{
        .value = &.{
            1,
            2,
        },
    };
    const my_data = &.{
        shared,
        shared,
    };
    _ = my_data;
}
