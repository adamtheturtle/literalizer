const Record0 = struct { x: i64 };
pub fn main() void {
    const my_data = &.{
        &.{},
        &.{Record0{ .x = 1 }},
    };
    _ = my_data;
}
