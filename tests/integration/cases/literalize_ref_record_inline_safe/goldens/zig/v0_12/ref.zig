const Record0 = struct { x: i64, y: ?i64 };
pub fn main() void {
    const my_data = Record0{
        .x = 1,
        .y = null,
    };
    _ = my_data;
}
