// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    let mut my_data: serde_json::Value = serde_json::json!({
        "a": 0,
    });
    consume_widget(my_data.clone());
    my_data = serde_json::json!({
        "a": 1,
    });
    consume_widget(my_data.clone());
}
