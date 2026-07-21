use std::collections::HashMap;
enum Value {
    I32(i32),
    Map(HashMap<String, String>),
}
fn main() {
    let my_data = vec![
        Value::I32(1),
        Value::Map(<HashMap<String, String>>::new()),
    ];
    let _ = my_data;
}
