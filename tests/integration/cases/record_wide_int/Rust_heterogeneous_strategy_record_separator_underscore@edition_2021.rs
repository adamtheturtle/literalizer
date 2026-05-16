use std::collections::HashMap;
struct Record0 {
    quantity: i32,
    big: i128,
    ratio: f64,
    label: &'static str,
    ok: bool,
}
fn main() {
    let my_data = Record0 {
        quantity: 1_000_000,
        big: 18_446_744_073_709_551_615i128,
        ratio: 2.5,
        label: "tag",
        ok: true,
    };
    let _ = my_data;
}
