use std::collections::HashMap;
#[derive(Clone)]
pub struct Record0 {
    pub name: Option<()>,
    pub id: i32,
}
fn main() {
    let my_data = HashMap::from([
        ("outer", [Record0 { name: None::<()>, id: 1 }]),
    ]);
    let _ = &my_data;
}
