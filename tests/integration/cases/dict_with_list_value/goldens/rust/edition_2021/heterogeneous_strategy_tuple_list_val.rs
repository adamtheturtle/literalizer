#[derive(Clone)]
pub struct Record0 {
    pub name: &'static str,
    pub scores: Vec<i32>,
}
fn main() {
    let my_data = Record0 {
        name: "Alice",
        scores: vec![
            10,
            20,
            30,
        ],
    };
    let _ = &my_data;
}
