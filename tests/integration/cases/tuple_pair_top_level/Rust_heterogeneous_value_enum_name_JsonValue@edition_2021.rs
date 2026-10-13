#[allow(dead_code)]
#[derive(Clone)]
enum JsonValue {
    I32(i32),
    Str(&'static str),
}
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        JsonValue::I32(1),
        JsonValue::Str("email"),
    ];
    let _ = &my_data;
}
