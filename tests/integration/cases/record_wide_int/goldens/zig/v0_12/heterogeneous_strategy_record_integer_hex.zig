const Record0 = struct { quantity: i64, big: u64, ratio: f64, label: []const u8, ok: bool };
pub fn main() void {
    const my_data = Record0{
        .quantity = 0xf4240,
        .big = 0xffffffffffffffff,
        .ratio = 2.5,
        .label = "tag",
        .ok = true,
    };
    _ = my_data;
}
