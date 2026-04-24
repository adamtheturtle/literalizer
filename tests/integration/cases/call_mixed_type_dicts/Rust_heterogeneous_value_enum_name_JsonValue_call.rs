use std::collections::HashMap;
enum JsonValue {
    Str(&'static str),
    Bool(bool),
}
fn main() {
    struct MgrType_;
    impl MgrType_ { fn op<A>(&self, _operation: A) {} }
    struct AppType_ { mgr: MgrType_ }
    let app = AppType_ { mgr: MgrType_ };
    app.mgr.op(HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_1")), ("draft", JsonValue::Bool(true))]));
    app.mgr.op(HashMap::from([("type", JsonValue::Str("create")), ("pr_id", JsonValue::Str("pr_2"))]));
}
