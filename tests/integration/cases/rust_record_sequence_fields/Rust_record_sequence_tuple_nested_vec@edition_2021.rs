#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    short: Vec<i32>,
    long: Vec<i32>,
}
#[allow(non_snake_case)]
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
