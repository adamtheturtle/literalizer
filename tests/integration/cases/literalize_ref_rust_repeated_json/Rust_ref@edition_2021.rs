// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
#[allow(non_snake_case)]
fn main() {
    let shared: serde_json::Value = serde_json::json!(42);
    let my_data: serde_json::Value = serde_json::json!([
        shared.clone(),
        shared.clone(),
    ]);
    let _ = &my_data;
}
