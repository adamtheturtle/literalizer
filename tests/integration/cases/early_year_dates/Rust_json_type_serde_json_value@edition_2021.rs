// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "date": "0099-05-27",
        "naive": "0001-01-01T12:30:00",
        "recent": "2024-05-27T10:00:00",
    });
    let _ = &my_data;
}
