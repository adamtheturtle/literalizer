use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
enum JsonValue {
    Str(&'static str),
    Bool(bool),
}
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_1")), ("draft", JsonValue::Bool(true))]),
        HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_2"))]),
    ];
    let _ = &my_data;
}
