#[derive(Clone)]
pub struct Record1 {
    pub a: i32,
    pub b: &'static str,
    pub c: Option<()>,
}
#[derive(Clone)]
pub struct Record0 {
    pub outer: Record1,
}
fn main() {
    let my_data = Record0 {
        outer: Record1 {
            a: 1,
            b: "x",
            c: None::<()>,
        },
    };
    let _ = &my_data;
}
