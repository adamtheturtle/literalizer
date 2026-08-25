// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        "2024-01-15",
        "2024-06-01",
    ]);
    let _ = my_data;
}
