#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
}
fn main() {
    let empty_items = Vec::new();
    let populated_items = vec![
        Record0 { x: 1 },
    ];
    let my_data = vec![
        empty_items,
        populated_items,
    ];
    let _ = &my_data;
}
