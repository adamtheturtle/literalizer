fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "name": "Alice",
        "score": null,
        "age": 30,
    });
    let _ = my_data;
}
