use std::collections::HashMap;
enum Value {
    Str(&'static str),
    Bool(bool),
    Null,
}
struct Record0 {
    name: &'static str,
    input: HashMap<&'static str, Value>,
    expected: HashMap<&'static str, Value>,
}
fn main() {
    let my_data = vec![
        Record0 { name: "test_1", input: HashMap::from([("type", Value::Str("create")), ("pr_id", Value::Str("pr_1")), ("draft", Value::Bool(true)), ("missing", Value::Null)]), expected: HashMap::from([("pr_id", Value::Str("pr_1")), ("status", Value::Str("draft"))]) },
        Record0 { name: "test_2", input: HashMap::from([("type", Value::Str("publish")), ("pr_id", Value::Str("pr_1"))]), expected: HashMap::from([("error", Value::Str("invalid_operation"))]) },
    ];
    let _ = my_data;
}
