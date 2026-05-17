const Record0 = struct { title: []const u8, tags: []const []const u8, priority: i64 };
pub fn main() void {
    const my_data = Record0{
        .title = "report",
        .tags = &.{
            "draft",
            "urgent",
            "review",
        },
        .priority = 2,
    };
    _ = my_data;
}
