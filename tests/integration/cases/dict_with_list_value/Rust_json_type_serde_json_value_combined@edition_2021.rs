fn main() {
    let mut my_data: serde_json::Value = serde_json::json!({
        "name": "Alice",
        "scores": serde_json::json!([10, 20, 30]),
    });
    my_data = serde_json::json!({
        "name": "Alice",
        "scores": serde_json::json!([10, 20, 30]),
    });
    let _ = my_data;
}
