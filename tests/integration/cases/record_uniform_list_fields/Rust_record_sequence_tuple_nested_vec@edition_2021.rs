#[derive(Clone)]
pub struct Record0 {
    pub scores: Vec<i32>,
}
fn main() {
    let my_data = vec![
        Record0 { scores: vec![1, 2] },
        Record0 { scores: vec![3, 4] },
    ];
    let _ = &my_data;
}
