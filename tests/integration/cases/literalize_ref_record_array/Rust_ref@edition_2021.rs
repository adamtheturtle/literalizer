#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
}
fn main() {
    let first = vec![
        Record0 { x: 1 },
        Record0 { x: 2 },
    ];
    let my_data = first;
    let _ = &my_data;
}
