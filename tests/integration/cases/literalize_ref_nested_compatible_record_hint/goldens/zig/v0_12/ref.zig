const Record1 = struct { items: []const i64 };
const Record0 = struct { outer: Record1 };
pub fn main() void {
    const record_data = Record1{
        .items = &.{
            1,
            2,
        },
    };
    const my_data = Record0{
        .outer = record_data,
    };
    _ = my_data;
}
