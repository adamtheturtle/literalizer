// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!({
        "$key": "a\"b\tcé #{world} $ident",
        "trailing multi-byte": "café",
    });
    let _ = my_data;
}
