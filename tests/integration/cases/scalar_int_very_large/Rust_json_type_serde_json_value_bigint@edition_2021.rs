fn main() {
    let my_data: serde_json::Value = serde_json::json!(9223372036854775808i128);
    let _ = my_data;
}
