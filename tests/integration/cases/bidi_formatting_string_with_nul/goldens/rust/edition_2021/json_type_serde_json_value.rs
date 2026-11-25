// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "v": "a\u{202A}\0é😀b",
    });
    let _ = &my_data;
}
