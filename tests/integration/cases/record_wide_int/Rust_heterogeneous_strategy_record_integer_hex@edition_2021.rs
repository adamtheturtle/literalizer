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
        quantity: 0xf4240,
        big: 0xffffffffffffffffi128,
        ratio: 2.5,
        label: "tag",
        ok: true,
    };
    let _ = my_data;
}
