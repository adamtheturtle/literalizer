use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
enum JsonValue {
    Str(&'static str),
    Bool(bool),
}
#[allow(non_snake_case)]
fn main() {
    struct MgrType;
    impl MgrType { fn run<A>(&self, _operation: A) {} }
    struct AppType { mgr: MgrType }
    let app = AppType { mgr: MgrType };
    app.mgr.run(HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_1")), ("draft", JsonValue::Bool(true))]));
    app.mgr.run(HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_2"))]));
}
