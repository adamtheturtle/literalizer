// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let ref_data: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let my_data: serde_json::Value = serde_json::json!(ref_data);
    let _ = &my_data;
}
