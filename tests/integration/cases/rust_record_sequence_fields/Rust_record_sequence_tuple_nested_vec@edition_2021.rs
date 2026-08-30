use std::collections::HashMap;
struct Record0 {
    short: Vec<i32>,
    long: Vec<i32>,
}
fn main() {
    let my_data = HashMap::from([
        ("short", vec![1]),
        ("long", vec![1, 2]),
    ]);
    let _ = my_data;
}
