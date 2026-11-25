const Record0 = struct { name: ?i64, id: i64 };
pub fn main() void {
    const my_data = &.{
        .{ .key = "outer", .val = &.{Record0{ .name = null, .id = 1 }} },
    };
    _ = my_data;
}
