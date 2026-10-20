const Record0 = struct { x: i64 };
pub fn main() void {
    const first = &.{
        Record0{ .x = 1 },
        Record0{ .x = 2 },
    };
    const my_data = first;
    _ = my_data;
}
