enum JsonValue {
    I32(i32),
    Str(&'static str),
    Bool(bool),
}
fn main() {
    let my_data = vec![
        JsonValue::I32(1),
        JsonValue::Str("email"),
        JsonValue::Bool(true),
    ];
    let _ = my_data;
}
