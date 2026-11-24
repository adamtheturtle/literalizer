// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn process<A>(_data: A) {}
    let unknown_value: serde_json::Value = serde_json::json!([]);
    process(serde_json::json!([unknown_value.clone()]));
}
