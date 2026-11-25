const Record0 = struct { s: []const u8, i: i64, f: f64, b: bool, n: ?i64, d: i64, dt: i64, by: []const u8 };
pub fn main() void {
    const my_data = Record0{
        .s = "string",
        .i = 1,
        .f = 1.5,
        .b = true,
        .n = null,
        .d = 1705276800,
        .dt = 1705320000,
        .by = "48656c6c6f",
    };
    _ = my_data;
}
