// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        -42,
        0,
        42,
        -1.25,
        0.0,
        1.25,
    ]);
    let _ = &my_data;
}
