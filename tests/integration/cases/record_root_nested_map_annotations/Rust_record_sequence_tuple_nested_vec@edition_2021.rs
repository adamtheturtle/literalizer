use std::collections::HashMap;
#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
}
fn main() {
    let my_data = HashMap::from([
        ("outer", vec![HashMap::from([("inner", Record0 { x: 1 })]), HashMap::from([("inner", Record0 { x: 2 })])]),
    ]);
    let _ = &my_data;
}
