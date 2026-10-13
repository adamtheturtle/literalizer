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
        ("a", JsonValue::I32(1)),
        ("b", JsonValue::Str("x")),
    ]);
    let _ = &my_data;
}
