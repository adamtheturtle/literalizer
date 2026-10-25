// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "quote\"backslash\\": 1,
        "line\nbreak": 2,
        "$(literal)${text}": 3,
        "RStr prefix": 4,
    });
    let _ = &my_data;
}
