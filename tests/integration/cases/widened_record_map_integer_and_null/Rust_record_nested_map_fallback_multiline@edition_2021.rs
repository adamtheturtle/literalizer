use std::collections::HashMap;
#[derive(Clone)]
enum Value {
    I32(i32),
    Null,
}
#[derive(Clone)]
struct Record0 {
    input: HashMap<&'static str, Value>,
}
fn main() {
    let my_data = vec![
        Record0 {
            input: HashMap::from([
                ("a", Value::I32(1)),
            ]),
        },
        Record0 {
            input: HashMap::from([
                ("b", Value::Null),
            ]),
        },
    ];
    let _ = my_data;
}
