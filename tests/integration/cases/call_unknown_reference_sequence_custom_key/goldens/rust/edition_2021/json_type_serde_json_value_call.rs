// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn process<A>(_data: A) {}
    let untyped_value: serde_json::Value = serde_json::json!([]);
    process(serde_json::json!([untyped_value.clone(), untyped_value.clone()]));
}
