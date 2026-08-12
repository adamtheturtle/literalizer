fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        ")json": "x",
    });
    let _ = my_data;
}
