const Record0 = struct { id: i64, label: []const u8, tags: []const i64 };
pub fn main() void {
    const my_data = &.{
        Record0{ .id = 1, .label = "first", .tags = &.{} },
        Record0{ .id = 2, .label = "second", .tags = &.{} },
        Record0{ .id = 3, .label = "third", .tags = &.{} },
    };
    _ = my_data;
}
