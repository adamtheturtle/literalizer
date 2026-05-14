use std::collections::HashMap;
struct Record0 {
    a: i32,
    b: &'static str,
}
fn main() {
    let my_data = Record0 {
        a: 1,
        b: "x",
    };
    let _ = my_data;
}
