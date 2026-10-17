const Record0 = struct { value: i64 };
pub fn main() void {
    const my_data = Record0{
        .value = -0o1000000000000000000000,
    };
    _ = my_data;
}
