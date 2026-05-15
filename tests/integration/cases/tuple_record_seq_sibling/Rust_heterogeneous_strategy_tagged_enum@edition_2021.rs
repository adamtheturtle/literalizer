use std::collections::HashMap;
enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = HashMap::from([
        ("scores", vec![Value::I32(10), Value::I32(20), Value::I32(30)]),
        ("args", vec![Value::I32(1), Value::Str("email"), Value::Str("a@gmail.com"), Value::I32(100)]),
    ]);
    let _ = my_data;
}
