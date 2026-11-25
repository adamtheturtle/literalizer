const Record1 = struct { id: i64, label: []const u8 };
const Record0 = struct { name: []const u8, items: []const Record1 };
pub fn main() void {
    const my_data = Record0{
        .name = "box",
        .items = &.{
            Record1{
                .id = 1,
                .label = "first",
            },
            Record1{
                .id = 2,
                .label = "second",
            },
        },
    };
    _ = my_data;
}
