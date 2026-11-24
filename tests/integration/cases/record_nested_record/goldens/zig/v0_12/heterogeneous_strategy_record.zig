const Record1 = struct { name: []const u8, age: i64 };
const Record0 = struct { id: i64, owner: Record1 };
pub fn main() void {
    const my_data = Record0{
        .id = 1,
        .owner = Record1{
            .name = "Alice",
            .age = 30,
        },
    };
    _ = my_data;
}
