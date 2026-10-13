#[allow(dead_code)]
#[derive(Clone)]
enum JsonValue {
    I32(i32),
    Str(&'static str),
    Bool(bool),
}
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        JsonValue::I32(1),
        JsonValue::Str("email"),
        JsonValue::Bool(true),
    ];
    let _ = &my_data;
}
