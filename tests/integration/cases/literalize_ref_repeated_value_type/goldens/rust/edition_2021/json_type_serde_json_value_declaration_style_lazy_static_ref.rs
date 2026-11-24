// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
use std::sync::LazyLock;
fn main() {
    static SHARED: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!(42));
    static MY_DATA: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!([
        (*SHARED).clone(),
        (*SHARED).clone(),
    ]));
    let _ = &MY_DATA;
}
