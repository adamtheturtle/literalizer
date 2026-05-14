use std::collections::HashMap;
enum JsonValue {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = vec![
        HashMap::from([("id", JsonValue::I32(1)), ("label", JsonValue::Str("first"))]),
        HashMap::from([("id", JsonValue::I32(2)), ("label", JsonValue::Str("second"))]),
        HashMap::from([("id", JsonValue::I32(3)), ("label", JsonValue::Str("third"))]),
    ];
    let _ = my_data;
}
