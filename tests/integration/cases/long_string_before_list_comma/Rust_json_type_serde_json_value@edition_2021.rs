// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
        1,
    ]);
    let _ = &my_data;
}
