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
        quantity: 0b11110100001001000000,
        big: 0b1111111111111111111111111111111111111111111111111111111111111111i128,
        ratio: 2.5,
        label: "tag",
        ok: true,
    };
    let _ = my_data;
}
