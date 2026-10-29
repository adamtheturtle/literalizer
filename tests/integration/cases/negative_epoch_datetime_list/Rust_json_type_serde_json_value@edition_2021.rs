// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        "1960-01-01T00:00:00+00:00",
    ]);
    let _ = &my_data;
}
