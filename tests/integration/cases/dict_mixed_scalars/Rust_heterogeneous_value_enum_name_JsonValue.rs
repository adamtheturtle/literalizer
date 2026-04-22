use std::collections::HashMap;
enum JsonValue {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = HashMap::from([
        ("a", JsonValue::I32(1)),
        ("b", JsonValue::Str("x")),
    ]);
    let _ = my_data;
}
