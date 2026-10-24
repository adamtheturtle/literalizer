// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        "1901-12-13T20:45:51",
        "1901-12-13T20:45:52",
        "2038-01-19T03:14:07",
        "2038-01-19T03:14:08",
    ]);
    let _ = &my_data;
}
