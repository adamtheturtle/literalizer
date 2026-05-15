use std::collections::HashMap;
struct Record0 {
    a: i32,
    b: i64,
    c: &'static str,
}
fn main() {
    let my_data = Record0 {
        a: 1,
        b: 3000000000i64,
        c: "x",
    };
    let _ = my_data;
}
