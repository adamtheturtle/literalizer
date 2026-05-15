use std::collections::HashMap;
struct Record0 {
    scores: Vec<i32>,
    args: (i32, &'static str, &'static str, i32),
}
fn main() {
    let my_data = Record0 {
        scores: vec![
            10,
            20,
            30,
        ],
        args: (
            1,
            "email",
            "a@gmail.com",
            100,
        ),
    };
    let _ = my_data;
}
