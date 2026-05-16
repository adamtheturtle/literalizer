const Record0 = struct { quantity: i64, big: u64, ratio: f64, label: []const u8, ok: bool };
pub fn main() void {
    const my_data = Record0{
        .quantity = 0b11110100001001000000,
        .big = 0b1111111111111111111111111111111111111111111111111111111111111111,
        .ratio = 2.5,
        .label = "tag",
        .ok = true,
    };
    _ = my_data;
}
