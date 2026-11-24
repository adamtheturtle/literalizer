#[derive(Clone)]
pub struct Record0 {
    pub value: i64,
}
fn main() {
    let my_data = Record0 {
        value: 2147483648i64,
    };
    let _ = &my_data;
}
