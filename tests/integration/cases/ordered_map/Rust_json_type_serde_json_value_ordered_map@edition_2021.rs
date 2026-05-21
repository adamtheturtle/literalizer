fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "name": "Alice",
        "age": 30,
        "active": true,
    });
    let _ = my_data;
}
