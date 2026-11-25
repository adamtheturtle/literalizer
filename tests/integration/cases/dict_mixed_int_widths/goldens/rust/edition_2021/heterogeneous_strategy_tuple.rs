#[derive(Clone)]
pub struct Record0 {
    pub a: i32,
    pub b: i64,
    pub c: &'static str,
}
fn main() {
    let my_data = Record0 {
        a: 1,
        b: 3000000000i64,
        c: "x",
    };
    let _ = &my_data;
}
