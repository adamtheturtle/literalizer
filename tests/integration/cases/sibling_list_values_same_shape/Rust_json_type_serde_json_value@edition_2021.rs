// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "test": serde_json::json!([5, serde_json::json!(["compile", "test"])]),
        "package": serde_json::json!([7, serde_json::json!(["link", "test"])]),
    });
    let _ = &my_data;
}
