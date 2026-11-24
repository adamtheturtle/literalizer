const Record1 = struct { count: i64, rate: i64 };
const Record2 = struct { retries: i64, timeout: i64 };
const Record0 = struct { metrics: Record1, flags: Record2 };
pub fn main() void {
    const my_data = Record0{
        .metrics = Record1{
            .count = 100,
            .rate = 50,
        },
        .flags = Record2{
            .retries = 3,
            .timeout = 30,
        },
    };
    _ = my_data;
}
