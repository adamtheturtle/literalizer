const Record0 = struct { a: i64 };
pub fn main() void {
    const my_data = &.{
        &.{Record0{ .a = 1 }},
        &.{Record0{ .a = 2 }},
    };
    _ = my_data;
}
