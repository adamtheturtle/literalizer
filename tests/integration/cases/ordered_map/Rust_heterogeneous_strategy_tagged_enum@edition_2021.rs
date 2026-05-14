use std::collections::HashMap;
enum Value {
    Str(&'static str),
    I32(i32),
    Bool(bool),
}
fn main() {
    let my_data = HashMap::from([
        ("name", Value::Str("Alice")),
        ("age", Value::I32(30)),
        ("active", Value::Bool(true)),
    ]);
    let _ = my_data;
}
