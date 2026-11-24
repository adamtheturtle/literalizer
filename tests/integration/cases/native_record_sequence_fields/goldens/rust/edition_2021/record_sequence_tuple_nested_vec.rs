#[derive(Clone)]
pub struct Record0 {
    pub short: Vec<i32>,
    pub long: Vec<i32>,
}
fn main() {
    let my_data = Record0 {
        short: vec![
            1,
        ],
        long: vec![
            1,
            2,
        ],
    };
    let _ = &my_data;
}
