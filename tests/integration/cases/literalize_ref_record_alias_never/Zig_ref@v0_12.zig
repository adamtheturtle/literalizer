const Record0 = struct { x: i64, y: ?i64 };
pub fn main() void {
    const value = Record0{
        .x = 1,
        .y = null,
    };
    const my_data = value;
    _ = my_data;
}
