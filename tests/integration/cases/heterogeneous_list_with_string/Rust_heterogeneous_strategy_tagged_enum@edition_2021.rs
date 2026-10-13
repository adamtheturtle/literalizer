#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    Str(&'static str),
    I32(i32),
}
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        Value::Str("hello"),
        Value::I32(42),
    ];
    let _ = &my_data;
}
