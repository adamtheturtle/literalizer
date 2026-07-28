use std::collections::HashMap;
enum Value {
    Str(&'static str),
}
struct Record1 {
    r#type: Option<&'static str>,
    pr_id: &'static str,
    draft: Option<bool>,
    missing: Option<Option<()>>,
    status: Option<Option<()>>,
}
struct Record0 {
    name: &'static str,
    input: Record1,
    expected: HashMap<&'static str, Value>,
}
fn main() {
    let my_data = vec![
        Record0 { name: "test_1", input: Record1 { r#type: Some("create"), pr_id: "pr_1", draft: Some(true), missing: Some(None::<()>), status: None }, expected: HashMap::from([("pr_id", Value::Str("pr_1")), ("status", Value::Str("draft"))]) },
        Record0 { name: "test_2", input: Record1 { r#type: Some("publish"), pr_id: "pr_1", draft: None, missing: None, status: None }, expected: HashMap::from([("error", Value::Str("invalid_operation"))]) },
    ];
    let _ = my_data;
}
