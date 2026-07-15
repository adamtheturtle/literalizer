use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<serde_json::Value> = LazyLock::new(|| serde_json::json!({
        "name": "Alice",
        "scores": serde_json::json!([10, 20, 30]),
    }));
    let _ = my_data;
}
