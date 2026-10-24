// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let arena: serde_json::Value = serde_json::json!({
        "a": 1,
    });
    let _ = &arena;
}
