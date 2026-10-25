// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let shared: serde_json::Value = serde_json::json!({
        "field": serde_json::json!([1, 2]),
    });
    let my_data: serde_json::Value = shared;
    let _ = &my_data;
}
