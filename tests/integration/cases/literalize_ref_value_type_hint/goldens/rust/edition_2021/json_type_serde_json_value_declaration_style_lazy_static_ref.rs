// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
use std::sync::LazyLock;
fn main() {
    static REF_DATA: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!([
        1,
        2,
    ]));
    static MY_DATA: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!((*REF_DATA).clone()));
    let _ = &MY_DATA;
}
