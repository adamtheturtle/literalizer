// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn process<A>(_value: A) {}
    let arena: serde_json::Value = serde_json::json!({
        "a": 1,
    });
    let ZVal: serde_json::Value = serde_json::json!({
        "a": 1,
    });
    let ZKV: serde_json::Value = serde_json::json!({
        "a": 1,
    });
    process(arena.clone());
    process(ZVal.clone());
    process(ZKV.clone());
}
