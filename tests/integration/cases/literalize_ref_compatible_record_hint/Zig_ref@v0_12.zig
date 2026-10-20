const Record0 = struct { items: []const i64 };
pub fn main() void {
    const record_data = Record0{
        .items = &.{
            1,
            2,
        },
    };
    const my_data = record_data;
    _ = my_data;
}
