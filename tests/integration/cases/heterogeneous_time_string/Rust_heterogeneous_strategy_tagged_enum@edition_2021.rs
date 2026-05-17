use std::collections::HashMap;
enum Value {
    Time(&'static str),
    Str(&'static str),
}
fn main() {
    let my_data = HashMap::from([
        ("vals", vec![Value::Time("09:30:00"), Value::Str("hello")]),
    ]);
    let _ = my_data;
}
