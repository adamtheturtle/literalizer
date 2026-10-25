// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
use std::sync::LazyLock;
fn main() {
    static SHARED: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!([
        1,
        2,
    ]));
    static BUILD: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!([
        1,
        2,
    ]));
    static JSON_OBJECT: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!([
        1,
        2,
    ]));
    static JSON_ALLOCATOR: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!([
        1,
        2,
    ]));
    static JSON_ENTRIES: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!([
        1,
        2,
    ]));
    static JSON_ENTRY: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!([
        1,
        2,
    ]));
    static MY_DATA: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!({
        "field": (*SHARED).clone(),
        "nested": serde_json::json!([(*SHARED).clone(), serde_json::json!({})]),
        "build": (*BUILD).clone(),
        "json_object": (*JSON_OBJECT).clone(),
        "json_allocator": (*JSON_ALLOCATOR).clone(),
        "json_entries": (*JSON_ENTRIES).clone(),
        "json_entry": (*JSON_ENTRY).clone(),
    }));
    let _ = &MY_DATA;
}
