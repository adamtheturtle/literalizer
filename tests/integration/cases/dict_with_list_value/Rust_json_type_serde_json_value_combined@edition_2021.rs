// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
#[allow(non_snake_case)]
fn main() {
    let mut my_data: serde_json::Value = serde_json::json!({
        "name": "Alice",
        "scores": serde_json::json!([10, 20, 30]),
    });
    let _ = &my_data;
    my_data = serde_json::json!({
        "name": "Alice",
        "scores": serde_json::json!([10, 20, 30]),
    });
    let _ = &mut my_data;
}
