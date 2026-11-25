const Record0 = struct { name: []const u8, scores: []const i64 };
pub fn main() void {
    const my_data = Record0{
        .name = "Alice",
        .scores = &.{
            10,
            20,
            30,
        },
    };
    _ = my_data;
}
