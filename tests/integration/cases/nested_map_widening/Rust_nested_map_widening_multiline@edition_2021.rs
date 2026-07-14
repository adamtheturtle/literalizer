use std::collections::HashMap;
enum Value {
    Str(&'static str),
    Bool(bool),
}
fn main() {
    let my_data = vec![
        HashMap::from([
            ("input", HashMap::from([
                ("kind", Value::Str("add")),
                ("item_id", Value::Str("item_1")),
                ("urgent", Value::Bool(true)),
            ])),
            ("expected", HashMap::from([
                ("item_id", Value::Str("item_1")),
                ("state", Value::Str("pending")),
            ])),
        ]),
        HashMap::from([
            ("input", HashMap::from([
                ("kind", Value::Str("remove")),
                ("item_id", Value::Str("item_9")),
            ])),
            ("expected", HashMap::from([
                ("error", Value::Str("not_found")),
            ])),
        ]),
    ];
    let _ = my_data;
}
