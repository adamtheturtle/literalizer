use std::collections::HashMap;
#[derive(Clone)]
pub struct Record0 {
    pub replacement: i32,
    pub present: i32,
}
fn main() {
    let my_data = HashMap::from([
        ("rows", vec![Record0 { replacement: -1, present: 1 }, Record0 { replacement: 2, present: 3 }]),
    ]);
    let _ = &my_data;
}
