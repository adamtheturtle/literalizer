// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn consume<A>(_value: A) {}
    let my_null: serde_json::Value = serde_json::json!(null);
    let regular_null: serde_json::Value = serde_json::json!(null);
    consume(my_null);
    consume(regular_null);
}
