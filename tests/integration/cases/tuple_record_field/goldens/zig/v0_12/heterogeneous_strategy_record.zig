const Record0 = struct { call: []const u8, args: struct { i64, []const u8, []const u8, i64 } };
pub fn main() void {
    const my_data = Record0{
        .call = "send",
        .args = .{
            1,
            "email",
            "a@gmail.com",
            100,
        },
    };
    _ = my_data;
}
