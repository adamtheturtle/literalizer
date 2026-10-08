use std::collections::HashMap;
enum Value {
    Null,
}
struct Record0 {
    input: HashMap<&'static str, Value>,
}
fn main() {
    let my_data = vec![
        Record0 { input: HashMap::from([("a", Value::Null)]) },
        Record0 { input: HashMap::from([("b", Value::Null)]) },
    ];
    let _ = my_data;
}
