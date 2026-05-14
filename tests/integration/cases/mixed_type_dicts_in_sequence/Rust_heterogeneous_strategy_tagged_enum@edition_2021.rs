use std::collections::HashMap;
enum Value {
    Str(&'static str),
    Bool(bool),
}
fn main() {
    let my_data = vec![
        HashMap::from([("type", Value::Str("create")), ("pr_id", Value::Str("pr_1")), ("draft", Value::Bool(true))]),
        HashMap::from([("type", Value::Str("create")), ("pr_id", Value::Str("pr_2"))]),
    ];
    let _ = my_data;
}
