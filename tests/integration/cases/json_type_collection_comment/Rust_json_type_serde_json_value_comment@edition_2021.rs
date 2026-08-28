// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "a": 1,  // About a.
        "b": 2,
    });
    let _ = my_data;
}
