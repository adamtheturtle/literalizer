const Record0 = struct { id: i64 };
pub fn main() void {
    const my_data = &.{
        .{ .key = "first", .val = &.{Record0{ .id = 1 }} },
        .{ .key = "second", .val = 2 },
    };
    _ = my_data;
}
