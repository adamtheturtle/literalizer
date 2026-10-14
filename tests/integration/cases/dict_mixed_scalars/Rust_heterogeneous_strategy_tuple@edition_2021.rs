#[derive(Clone)]
pub struct Record0 {
    pub a: i32,
    pub b: &'static str,
}
fn main() {
    let my_data = Record0 {
        a: 1,
        b: "x",
    };
    let _ = &my_data;
}
