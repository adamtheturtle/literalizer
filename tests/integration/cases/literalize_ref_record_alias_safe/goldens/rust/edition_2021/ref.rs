#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
    pub y: Option<()>,
}
fn main() {
    let value = Record0 {
        x: 1,
        y: None::<()>,
    };
    let my_data = value;
    let _ = &my_data;
}
