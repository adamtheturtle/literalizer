const Record0 = struct { within_i32: i64, beyond_i32: i64 };
pub fn main() void {
    const my_data = Record0{
        .within_i32 = 1705320000,
        .beyond_i32 = 4085195400,
    };
    _ = my_data;
}
