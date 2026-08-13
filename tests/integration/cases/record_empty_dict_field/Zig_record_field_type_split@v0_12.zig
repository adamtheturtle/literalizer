const Record0 = struct { f: []const u8, g: i64 };
pub fn main() void {
    const my_data = Record0{
        .f = .{},
        .g = 1,
    };
    _ = my_data;
}
