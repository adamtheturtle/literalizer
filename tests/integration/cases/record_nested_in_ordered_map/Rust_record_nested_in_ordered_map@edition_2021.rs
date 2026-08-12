use std::collections::HashMap;
struct Record0 {
    name: Option<()>,
    id: i32,
}
fn main() {
    let my_data = HashMap::from([
        ("outer", [Record0 { name: None::<()>, id: 1 }]),
    ]);
    let _ = my_data;
}
