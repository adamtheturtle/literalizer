const Record0 = struct { labels: []const []const u8 };
pub fn main() void {
    const first = Record0{
        .labels = &.{
            "owned",
        },
    };
    const my_data = first;
    _ = my_data;
}
