#[derive(Clone)]
pub struct Record0 {
    pub a: i32,
}
fn main() {
    let ZKV = Record0 {
        a: 1,
    };
    let _ = &ZKV;
}
