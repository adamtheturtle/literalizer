use std::collections::HashMap;
struct Record1 {
    a: i32,
    b: &'static str,
    c: Option<()>,
}
struct Record0 {
    outer: Record1,
}
fn main() {
    let my_data = Record0 {
        outer: Record1 {
            a: 1,
            b: "x",
            c: None::<()>,
        },
    };
    let _ = my_data;
}
