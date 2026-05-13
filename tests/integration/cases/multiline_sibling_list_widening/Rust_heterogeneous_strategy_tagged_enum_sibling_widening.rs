use std::collections::HashMap;
enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = HashMap::from([
        ("omap_value", HashMap::from([("first", 1)])),
        ("sibling_lists", HashMap::from([("numbers", vec![Value::I32(1), Value::I32(2)]), ("strings", vec![Value::Str("x"), Value::Str("y")])])),
        ("ref_marker_present", vec!["$keep", "z"]),
    ]);
    let _ = my_data;
}
