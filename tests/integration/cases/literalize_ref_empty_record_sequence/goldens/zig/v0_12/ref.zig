const Record0 = struct { x: i64 };
pub fn main() void {
    const empty_items = &.{};
    const populated_items = &.{
        Record0{ .x = 1 },
    };
    const my_data = &.{
        empty_items,
        populated_items,
    };
    _ = my_data;
}
