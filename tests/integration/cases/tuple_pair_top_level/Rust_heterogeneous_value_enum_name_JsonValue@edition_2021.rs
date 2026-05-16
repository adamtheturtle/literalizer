enum JsonValue {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = vec![
        JsonValue::I32(1),
        JsonValue::Str("email"),
    ];
    let _ = my_data;
}
