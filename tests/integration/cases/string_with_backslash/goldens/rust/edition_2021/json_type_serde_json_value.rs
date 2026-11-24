// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
        "path\\to \"# file",
        "trailing\\",
        "both \"quotes''' here",
        "line1\\nline2\nwith newline",
    ]);
    let _ = &my_data;
}
