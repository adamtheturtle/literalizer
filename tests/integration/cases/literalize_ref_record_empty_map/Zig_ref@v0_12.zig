const Record0 = struct { bound: []const u8 };
pub fn main() void {
    const empty_map = .{};
    const my_data = Record0{
        .bound = empty_map,
    };
    _ = my_data;
}
