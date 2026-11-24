// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn consume<A>(_value: A) {}
    let shared: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    consume(serde_json::json!([shared.clone(), shared.clone()]));
}
