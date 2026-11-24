const Record0 = struct { a: i64, b: i64, c: []const u8 };
pub fn main() void {
    const my_data = Record0{
        .a = 1,
        .b = 3000000000,
        .c = "x",
    };
    _ = my_data;
}
