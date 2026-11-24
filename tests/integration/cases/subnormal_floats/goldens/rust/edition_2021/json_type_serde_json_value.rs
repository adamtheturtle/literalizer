// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        5.0e-324,
        -5.0e-324,
        1.0e-310,
    ]);
    let _ = &my_data;
}
