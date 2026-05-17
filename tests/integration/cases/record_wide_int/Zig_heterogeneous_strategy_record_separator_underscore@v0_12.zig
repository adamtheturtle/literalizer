const Record0 = struct { quantity: i64, big: u64, ratio: f64, label: []const u8, ok: bool };
pub fn main() void {
    const my_data = Record0{
        .quantity = 1_000_000,
        .big = 18_446_744_073_709_551_615,
        .ratio = 2.5,
        .label = "tag",
        .ok = true,
    };
    _ = my_data;
}
