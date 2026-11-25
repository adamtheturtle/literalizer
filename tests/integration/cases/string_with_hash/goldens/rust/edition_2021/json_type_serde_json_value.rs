// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        "issue #{42}",
        "color #red",
    ]);
    let _ = &my_data;
}
