// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        serde_json::json!({"values": serde_json::json!([])}),
        serde_json::json!({}),
    ]);
    let _ = &my_data;
}
