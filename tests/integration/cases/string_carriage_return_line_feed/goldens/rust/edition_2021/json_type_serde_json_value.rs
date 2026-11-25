// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "cr": "a\rb",
        "crlf": "a\r\nb",
        "lf": "a\nb",
    });
    let _ = &my_data;
}
