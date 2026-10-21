// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    fn make_widget<A>(_value: A) {}
    make_widget(serde_json::json!([]));
}
