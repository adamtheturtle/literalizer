// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "morning": "09:30:00",
        "afternoon": "14:15:00",
        "evening": "23:59:59",
    });
    let _ = &my_data;
}
