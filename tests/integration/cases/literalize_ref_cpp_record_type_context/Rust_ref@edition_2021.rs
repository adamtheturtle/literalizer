#[derive(Clone)]
pub struct Record1 {
    pub x: &'static str,
}
#[derive(Clone)]
pub struct Record2 {
    pub x: i32,
}
#[derive(Clone)]
pub struct Record0 {
    pub direct: Record1,
    pub bound: Record2,
}
fn main() {
    let first = Record2 {
        x: 1,
    };
    let my_data = Record0 {
        direct: Record1 {
            x: "s",
        },
        bound: first,
    };
    let _ = &my_data;
}
