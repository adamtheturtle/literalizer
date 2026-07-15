fn main() {
    let my_data: serde_json::Value = serde_json::json!("a\"b\tcé");
    let _ = my_data;
}
