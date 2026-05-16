const Record0 = struct { name: []const u8, age: i64, active: bool, score: f64 };
pub fn main() void {
    const my_data = Record0{
        .name = "Alice",
        .age = 30,
        .active = true,
        .score = 4.5,
    };
    _ = my_data;
}
