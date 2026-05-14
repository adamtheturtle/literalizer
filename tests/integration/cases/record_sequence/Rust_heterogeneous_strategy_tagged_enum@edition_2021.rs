use std::collections::HashMap;
enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = vec![
        HashMap::from([("id", Value::I32(1)), ("label", Value::Str("first"))]),
        HashMap::from([("id", Value::I32(2)), ("label", Value::Str("second"))]),
        HashMap::from([("id", Value::I32(3)), ("label", Value::Str("third"))]),
    ];
    let _ = my_data;
}
