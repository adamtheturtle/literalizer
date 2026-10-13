#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    I32(i32),
    Str(&'static str),
}
#[allow(non_snake_case)]
fn main() {
    let shared = [
        Value::I32(1),
        Value::Str("x"),
    ];
    let my_data = [
        shared.clone(),
        shared.clone(),
    ];
    let _ = &my_data;
}
