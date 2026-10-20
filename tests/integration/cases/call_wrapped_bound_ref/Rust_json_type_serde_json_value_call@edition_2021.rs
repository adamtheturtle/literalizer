// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn make_widget<A>(_value: A) {}
    let value: serde_json::Value = serde_json::json!(1);
    make_widget(value.clone());
}
