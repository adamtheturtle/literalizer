fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "$key": "a\"b\tcé #{world} $ident",
    });
    let _ = my_data;
}
