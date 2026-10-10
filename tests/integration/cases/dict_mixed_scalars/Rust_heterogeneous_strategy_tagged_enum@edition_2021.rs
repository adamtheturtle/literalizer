use std::collections::HashMap;
#[derive(Clone)]
enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = HashMap::from([
        ("a", Value::I32(1)),
        ("b", Value::Str("x")),
    ]);
    let _ = my_data;
}
