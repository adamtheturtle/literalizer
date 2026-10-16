// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    struct ThingType;
    impl ThingType { fn go<A>(&self, _value: A) {} }
    let thing = ThingType;
    let my_data: serde_json::Value = thing.go(serde_json::json!([1]));
    let _ = &my_data;
}
