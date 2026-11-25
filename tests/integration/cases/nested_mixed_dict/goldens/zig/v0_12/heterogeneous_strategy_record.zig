const Record1 = struct { a: i64, b: []const u8, c: ?i64 };
const Record0 = struct { outer: Record1 };
pub fn main() void {
    const my_data = Record0{
        .outer = Record1{
            .a = 1,
            .b = "x",
            .c = null,
        },
    };
    _ = my_data;
}
