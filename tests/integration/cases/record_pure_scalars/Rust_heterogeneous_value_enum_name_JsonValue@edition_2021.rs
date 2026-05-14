use std::collections::HashMap;
enum JsonValue {
    Str(&'static str),
    I32(i32),
    Bool(bool),
    F64(f64),
}
fn main() {
    let my_data = HashMap::from([
        ("name", JsonValue::Str("Alice")),
        ("age", JsonValue::I32(30)),
        ("active", JsonValue::Bool(true)),
        ("score", JsonValue::F64(4.5)),
    ]);
    let _ = my_data;
}
