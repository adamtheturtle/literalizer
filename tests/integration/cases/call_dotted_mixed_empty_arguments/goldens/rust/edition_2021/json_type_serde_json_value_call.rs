// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    struct ThingType;
    impl ThingType { fn go<A, B, C>(&self, _before: A, _populated: B, _after: C) {} }
    let thing = ThingType;
    thing.go(serde_json::json!([]), serde_json::json!([1]), serde_json::json!([]));
    thing.go(serde_json::json!(["text"]), serde_json::json!([2]), serde_json::json!([]));
    thing.go(serde_json::json!([]), serde_json::json!(["text"]), serde_json::json!([]));
    thing.go(serde_json::json!(["text"]), serde_json::json!([2]), serde_json::json!([3]));
}
