const Record0 = struct { vals: struct { []const u8, []const u8 } };
pub fn main() void {
    const my_data = Record0{
        .vals = .{
            "09:30:00",
            "hello",
        },
    };
    _ = my_data;
}
