// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "times": serde_json::json!(["09:30:00", "17:45:00", "23:59:59"]),
    });
    let _ = &my_data;
}
