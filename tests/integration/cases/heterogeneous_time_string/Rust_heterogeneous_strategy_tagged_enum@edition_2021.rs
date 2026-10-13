use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    Time(&'static str),
    Str(&'static str),
}
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("vals", vec![Value::Time("09:30:00"), Value::Str("hello")]),
    ]);
    let _ = &my_data;
}
