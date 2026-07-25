const Record0 = struct { id: i64, label: []const u8, enabled: bool, related_ids: []const i64 };
pub fn main() void {
    const my_data = Record0{
        .id = 1,
        .label = "She said \"hello\", then waved",
        .enabled = false,
        .related_ids = &.{
            1,
            2,
            3,
        },
    };
    _ = my_data;
}
