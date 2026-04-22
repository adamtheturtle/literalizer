use std::collections::HashMap;
enum Value {
    I32(i32),
    I64(i64),
    Str(&'static str),
}
fn main() {
    let my_data = HashMap::from([
        ("a", Value::I32(1)),
        ("b", Value::I64(3000000000i64)),
        ("c", Value::Str("x")),
    ]);
    let _ = my_data;
}
