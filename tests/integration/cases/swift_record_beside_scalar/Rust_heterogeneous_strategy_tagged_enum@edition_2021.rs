use std::collections::HashMap;
enum Value {
    I32(i32),
    Map(HashMap<&'static str, Value>),
}
fn main() {
    let my_data = vec![
        Value::Map(HashMap::from([("a", Value::I32(1))])),
        Value::I32(5),
    ];
    let _ = my_data;
}
