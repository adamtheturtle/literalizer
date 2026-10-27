// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "bounds": serde_json::json!([-9223372036854775808i128, 9223372036854775807i128, 9223372036854775808i128, 18446744073709551615i128]),
        "nested": serde_json::json!([serde_json::json!({"minimum": -9223372036854775808i128, "maximum": 18446744073709551615i128})]),
    });
    let _ = &my_data;
}
