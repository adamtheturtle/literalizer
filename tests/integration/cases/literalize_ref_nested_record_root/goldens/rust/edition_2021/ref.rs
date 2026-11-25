#[derive(Clone)]
pub struct Record1 {
    pub value: i32,
}
#[derive(Clone)]
pub struct Record0 {
    pub child: Record1,
}
fn main() {
    let first = Record0 {
        child: Record1 {
            value: 1,
        },
    };
    let my_data = first;
    let _ = &my_data;
}
