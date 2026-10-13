use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    name: Option<()>,
    id: i32,
}
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("outer", [Record0 { name: None::<()>, id: 1 }]),
    ]);
    let _ = &my_data;
}
