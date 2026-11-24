#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
    pub y: Option<()>,
}
fn main() {
    let my_data = Record0 {
        x: 1,
        y: None::<()>,
    };
    let _ = &my_data;
}
