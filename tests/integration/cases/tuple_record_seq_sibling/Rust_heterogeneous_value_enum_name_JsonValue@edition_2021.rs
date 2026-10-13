use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
enum JsonValue {
    I32(i32),
    Str(&'static str),
}
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("scores", vec![JsonValue::I32(10), JsonValue::I32(20), JsonValue::I32(30)]),
        ("args", vec![JsonValue::I32(1), JsonValue::Str("email"), JsonValue::Str("a@gmail.com"), JsonValue::I32(100)]),
    ]);
    let _ = &my_data;
}
