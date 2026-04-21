use std::collections::HashMap;
enum Value {
    I32(i32),
    Str(&'static str),
    Null,
}
fn main() {
    let my_data = HashMap::from([
        ("outer", HashMap::from([("a", Value::I32(1)), ("b", Value::Str("x")), ("c", Value::Null)])),
    ]);
    let _ = my_data;
}
