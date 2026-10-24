// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
#[derive(Clone)]
pub struct Record0 {
    pub a: i32,
}
fn main() {
    let ZVal = Record0 {
        a: 1,
    };
    let _ = &ZVal;
}
