fn main() {
    let my_data: serde_json::Value = serde_json::json!(2147483648i64);
    let _ = my_data;
}
