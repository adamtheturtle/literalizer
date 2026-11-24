// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    let my_data: serde_json::Value = serde_json::json!([
        serde_json::json!(["set_task", "web", "lint_web"]),
        serde_json::json!(["merge_pipelines"]),
    ]);
    let _ = &my_data;
}
