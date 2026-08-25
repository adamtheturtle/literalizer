// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        serde_json::json!([1, "a"]),
        serde_json::json!([2, "b"]),
    ]);
    let _ = my_data;
}
