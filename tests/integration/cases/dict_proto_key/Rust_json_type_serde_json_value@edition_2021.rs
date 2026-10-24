// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "__proto__": serde_json::json!({"x": 1}),
        "n": serde_json::json!({"__proto__": 3}),
        "y": 2,
    });
    let _ = &my_data;
}
