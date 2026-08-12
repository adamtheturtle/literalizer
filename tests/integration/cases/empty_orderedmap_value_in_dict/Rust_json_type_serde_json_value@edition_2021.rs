fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "a": serde_json::json!({}),
        "b": 1,
    });
    let _ = my_data;
}
