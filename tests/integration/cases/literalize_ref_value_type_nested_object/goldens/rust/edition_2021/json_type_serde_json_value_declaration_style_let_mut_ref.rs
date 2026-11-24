// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let mut shared: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let _ = &mut shared;
    let mut build: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let _ = &mut build;
    let mut json_object: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let _ = &mut json_object;
    let mut json_allocator: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let _ = &mut json_allocator;
    let mut json_entries: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let _ = &mut json_entries;
    let mut json_entry: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let _ = &mut json_entry;
    let mut my_data: serde_json::Value = serde_json::json!({
        "field": shared.clone(),
        "nested": serde_json::json!([shared.clone(), serde_json::json!({})]),
        "build": build,
        "json_object": json_object,
        "json_allocator": json_allocator,
        "json_entries": json_entries,
        "json_entry": json_entry,
    });
    let _ = &mut my_data;
}
