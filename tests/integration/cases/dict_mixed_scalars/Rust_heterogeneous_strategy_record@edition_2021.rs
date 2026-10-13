#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    a: i32,
    b: &'static str,
}
#[allow(non_snake_case)]
fn main() {
    let my_data = Record0 {
        a: 1,
        b: "x",
    };
    let _ = &my_data;
}
