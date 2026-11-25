const Record0 = struct { a: i64 };
pub fn main() void {
    const my_data = .{
        Record0{ .a = 1 },
        5,
    };
    _ = my_data;
}
