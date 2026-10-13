// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
#[allow(non_snake_case)]
fn main() {
    let my_data: serde_json::Value = serde_json::json!(1705321800);
    let _ = &my_data;
}
