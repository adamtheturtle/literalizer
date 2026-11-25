// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let mut ref_data: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let _ = &mut ref_data;
    let mut my_data: serde_json::Value = serde_json::json!(ref_data);
    let _ = &mut my_data;
}
