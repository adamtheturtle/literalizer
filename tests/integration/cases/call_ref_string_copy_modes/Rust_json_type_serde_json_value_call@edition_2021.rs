// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn consume<A>(_value: A) {}
    let item: serde_json::Value = serde_json::json!("s");
    consume(item);
}
