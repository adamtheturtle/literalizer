// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "long_str": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "quoted": "a\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"b",
        "wide": "中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中",
    });
    let _ = my_data;
}
