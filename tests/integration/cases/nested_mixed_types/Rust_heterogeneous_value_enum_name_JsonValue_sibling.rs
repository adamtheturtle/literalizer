enum JsonValue {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = vec![
        vec![JsonValue::I32(1), JsonValue::I32(2)],
        vec![JsonValue::Str("a"), JsonValue::Str("b")],
    ];
    let _ = my_data;
}
