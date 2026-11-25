use std::collections::HashMap;
#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
}
fn main() {
    let my_data = vec![
        HashMap::from([("first", Record0 { x: 1 })]),
        HashMap::from([("first", Record0 { x: 2 })]),
    ];
    let _ = &my_data;
}
