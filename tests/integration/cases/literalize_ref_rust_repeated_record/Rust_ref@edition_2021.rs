#[derive(Clone)]
pub struct Record0 {
    pub value: Vec<i32>,
}
fn main() {
    let shared = Record0 {
        value: vec![
            1,
            2,
        ],
    };
    let my_data = vec![
        shared.clone(),
        shared.clone(),
    ];
    let _ = &my_data;
}
