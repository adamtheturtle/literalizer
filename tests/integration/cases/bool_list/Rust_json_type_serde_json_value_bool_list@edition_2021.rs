fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        true,
        false,
        true,
    ]);
    let _ = my_data;
}
