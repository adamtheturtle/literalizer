#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    I32(i32),
    Str(&'static str),
    Bool(bool),
}
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        Value::I32(1),
        Value::Str("email"),
        Value::Bool(true),
    ];
    let _ = &my_data;
}
