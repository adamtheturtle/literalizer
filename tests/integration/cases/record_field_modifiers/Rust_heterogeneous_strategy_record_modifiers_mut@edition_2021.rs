#[derive(Clone)]
pub struct Record0 {
    pub one: i32,
}
fn main() {
    let mut my_data = Record0 {
        one: 1,
    };
    let _ = &mut my_data;
}
