#[derive(Clone)]
pub struct Record0 {
    pub items: Vec<i32>,
}
fn main() {
    let record_data = vec![
        Record0 { items: vec![1, 2] },
    ];
    let my_data = record_data;
    let _ = &my_data;
}
