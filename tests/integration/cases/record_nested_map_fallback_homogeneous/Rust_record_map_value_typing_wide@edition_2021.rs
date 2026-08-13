use std::collections::HashMap;
enum Value {
    Str(&'static str),
}
struct Record1 {
    kind: &'static str,
    pr_id: &'static str,
}
struct Record0 {
    name: &'static str,
    input: Record1,
    expected: HashMap<&'static str, Value>,
}
fn main() {
    let my_data = vec![
        Record0 { name: "test_1", input: Record1 { kind: "create", pr_id: "pr_1" }, expected: HashMap::from([("pr_id", Value::Str("pr_1")), ("status", Value::Str("draft"))]) },
        Record0 { name: "test_2", input: Record1 { kind: "publish", pr_id: "pr_1" }, expected: HashMap::from([("error", Value::Str("invalid_operation"))]) },
    ];
    let _ = my_data;
}
