enum JsonValue {
    Str(&'static str),
    I32(i32),
}
fn main() {
    let my_data = vec![
        JsonValue::Str("hello"),
        JsonValue::I32(42),
    ];
    let _ = my_data;
}
