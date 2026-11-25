use std::collections::HashMap;
#[derive(Clone)]
pub enum JsonValue {
    Str(&'static str),
    Bool(bool),
}
fn main() {
    struct MgrType;
    impl MgrType { fn run<A>(&self, _operation: A) {} }
    struct AppType { mgr: MgrType }
    let app = AppType { mgr: MgrType };
    app.mgr.run(HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_1")), ("draft", JsonValue::Bool(true))]));
    app.mgr.run(HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_2"))]));
}
