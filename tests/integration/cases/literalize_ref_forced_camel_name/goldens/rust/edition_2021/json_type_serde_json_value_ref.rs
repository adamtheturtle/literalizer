// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let userObj: serde_json::Value = serde_json::json!({
        "_": "_",
    });
    let my_data: serde_json::Value = userObj;
    let _ = &my_data;
}
