// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let mut shared: serde_json::Value = serde_json::json!(42);
    let _ = &mut shared;
    let mut my_data: serde_json::Value = serde_json::json!([
        shared.clone(),
        shared.clone(),
    ]);
    let _ = &mut my_data;
}
