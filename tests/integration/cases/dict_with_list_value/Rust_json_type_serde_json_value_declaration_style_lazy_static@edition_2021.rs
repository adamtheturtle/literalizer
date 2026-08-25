// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!({
        "name": "Alice",
        "scores": serde_json::json!([10, 20, 30]),
    }));
    let _ = my_data;
}
