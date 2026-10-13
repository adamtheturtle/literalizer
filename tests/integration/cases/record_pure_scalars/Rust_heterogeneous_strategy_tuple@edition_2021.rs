#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    name: &'static str,
    age: i32,
    active: bool,
    score: f64,
}
#[allow(non_snake_case)]
fn main() {
    let my_data = Record0 {
        name: "Alice",
        age: 30,
        active: true,
        score: 4.5,
    };
    let _ = &my_data;
}
