use std::collections::HashMap;
enum JsonValue {
    Str(&'static str),
    Bool(bool),
}
fn main() {
    let my_data = vec![
        HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_1")), ("draft", JsonValue::Bool(true))]),
        HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_2"))]),
    ];
    let _ = my_data;
}
