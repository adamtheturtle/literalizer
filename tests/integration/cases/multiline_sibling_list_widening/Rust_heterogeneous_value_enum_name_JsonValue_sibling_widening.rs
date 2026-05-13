use std::collections::HashMap;
enum JsonValue {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = HashMap::from([
        ("omap_value", HashMap::from([("first", 1)])),
        ("sibling_lists", HashMap::from([("numbers", vec![JsonValue::I32(1), JsonValue::I32(2)]), ("strings", vec![JsonValue::Str("x"), JsonValue::Str("y")])])),
        ("ref_marker_present", vec!["$keep", "z"]),
    ]);
    let _ = my_data;
}
