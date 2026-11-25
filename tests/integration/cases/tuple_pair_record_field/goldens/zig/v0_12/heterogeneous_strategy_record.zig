const Record0 = struct { call: []const u8, args: struct { i64, []const u8 } };
pub fn main() void {
    const my_data = Record0{
        .call = "send",
        .args = .{
            1,
            "email",
        },
    };
    _ = my_data;
}
