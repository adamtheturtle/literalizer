fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        serde_json::json!({"first": "Alice", "last": "Smith"}),
        serde_json::json!({"first": "Bob", "last": "Jones"}),
    ]);
    let _ = my_data;
}
