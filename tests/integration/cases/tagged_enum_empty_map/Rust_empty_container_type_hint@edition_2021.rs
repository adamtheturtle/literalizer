use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    I32(i32),
    Map(HashMap<String, String>),
}
fn main() {
    let my_data = vec![
        Value::I32(1),
        Value::Map(HashMap::new()),
    ];
    let _ = &my_data;
}
