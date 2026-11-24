// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    let item: serde_json::Value = serde_json::json!(null);
    let mut my_data: serde_json::Value = serde_json::json!(null);
    consume_widget(my_data.clone());
    my_data = serde_json::json!(item);
    consume_widget(my_data.clone());
}
