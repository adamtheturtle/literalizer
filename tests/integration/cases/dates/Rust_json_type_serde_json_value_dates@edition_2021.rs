fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "date": "2024-01-15",
        "datetime": "2024-01-15T12:30:00+00:00",
    });
    let _ = my_data;
}
