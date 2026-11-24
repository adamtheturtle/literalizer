const Record0 = struct { a: i64, b: []const u8 };
pub fn main() void {
    const my_data = Record0{
        .a = 1,
        .b = "x",
    };
    _ = my_data;
}
