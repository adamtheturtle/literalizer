#[derive(Clone)]
pub struct Record1 {
    pub items: Vec<i32>,
}
#[derive(Clone)]
pub struct Record0 {
    pub outer: Record1,
}
fn main() {
    let record_data = Record1 {
        items: vec![
            1,
            2,
        ],
    };
    let my_data = Record0 {
        outer: record_data,
    };
    let _ = &my_data;
}
