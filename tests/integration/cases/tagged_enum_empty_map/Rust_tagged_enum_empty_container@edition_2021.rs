use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    I32(i32),
    Map(HashMap<&'static str, Value>),
}
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        Value::I32(1),
        Value::Map(HashMap::new()),
    ];
    let _ = &my_data;
}
