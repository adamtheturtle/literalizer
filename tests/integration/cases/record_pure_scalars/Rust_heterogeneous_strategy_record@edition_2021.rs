use std::collections::HashMap;
struct Record0 {
    name: &'static str,
    age: i32,
    active: bool,
    score: f64,
}
fn main() {
    let my_data = Record0 {
        name: "Alice",
        age: 30,
        active: true,
        score: 4.5,
    };
    let _ = my_data;
}
