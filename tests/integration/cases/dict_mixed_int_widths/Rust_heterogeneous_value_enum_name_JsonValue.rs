use std::collections::HashMap;
enum JsonValue {
    I32(i32),
    I64(i64),
    Str(&'static str),
}
fn main() {
    let my_data = HashMap::from([
        ("a", JsonValue::I32(1)),
        ("b", JsonValue::I64(3000000000i64)),
        ("c", JsonValue::Str("x")),
    ]);
    let _ = my_data;
}
