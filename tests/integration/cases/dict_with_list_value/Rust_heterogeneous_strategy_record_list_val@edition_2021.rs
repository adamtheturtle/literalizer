use std::collections::HashMap;
struct Record0 {
    name: &'static str,
    scores: Vec<i32>,
}
fn main() {
    let my_data = Record0 {
        name: "Alice",
        scores: vec![
            10,
            20,
            30,
        ],
    };
    let _ = my_data;
}
