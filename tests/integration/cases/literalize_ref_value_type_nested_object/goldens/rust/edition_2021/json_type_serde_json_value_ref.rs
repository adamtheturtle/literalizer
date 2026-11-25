// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let shared: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let build: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let json_object: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let json_allocator: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let json_entries: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let json_entry: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let my_data: serde_json::Value = serde_json::json!({
        "field": shared.clone(),
        "nested": serde_json::json!([shared.clone(), serde_json::json!({})]),
        "build": build,
        "json_object": json_object,
        "json_allocator": json_allocator,
        "json_entries": json_entries,
        "json_entry": json_entry,
    });
    let _ = &my_data;
}
