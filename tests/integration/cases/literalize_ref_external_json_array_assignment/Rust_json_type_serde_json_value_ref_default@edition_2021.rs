// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    let shared: serde_json::Value = serde_json::json!([
        1,
        2,
    ]);
    let mut my_data: serde_json::Value = serde_json::json!([
        0,
    ]);
    consume_widget(my_data.clone());
    my_data = shared;
    consume_widget(my_data.clone());
}
