const Record0 = struct { x: i64 };
pub fn main() void {
    const my_data = .{
        .{&.{1}, Record0{ .x = 1 }},
        &.{Record0{ .x = 1 }, Record0{ .x = 2 }},
        &.{&.{}, &.{Record0{ .x = 1 }}},
        .{&.{}, &.{}},
    };
    _ = my_data;
}
