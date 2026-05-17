const Record0 = struct { id: i64, description: []const u8, is_done: bool, blocks: []const i64 };
pub fn main() void {
    const my_data = Record0{
        .id = 1,
        .description = "She said \"hello\", then waved",
        .is_done = false,
        .blocks = &.{
            1,
            2,
            3,
        },
    };
    _ = my_data;
}
