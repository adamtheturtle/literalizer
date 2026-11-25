// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "exact_millisecond": "09:30:15.123000",
        "sub_millisecond": "09:30:15.123456",
    });
    let _ = &my_data;
}
