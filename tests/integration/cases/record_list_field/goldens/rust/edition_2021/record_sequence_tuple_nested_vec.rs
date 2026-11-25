#[derive(Clone)]
pub struct Record1 {
    pub a: i32,
}
#[derive(Clone)]
pub struct Record0 {
    pub items: Vec<Record1>,
}
fn main() {
    let my_data = Record0 {
        items: vec![
            Record1 {
                a: 1,
            },
        ],
    };
    let _ = &my_data;
}
