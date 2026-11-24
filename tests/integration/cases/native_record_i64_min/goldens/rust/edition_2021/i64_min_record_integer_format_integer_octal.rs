#[derive(Clone)]
pub struct Record0 {
    pub value: i64,
}
fn main() {
    let my_data = Record0 {
        value: -0o1000000000000000000000i64,
    };
    let _ = &my_data;
}
