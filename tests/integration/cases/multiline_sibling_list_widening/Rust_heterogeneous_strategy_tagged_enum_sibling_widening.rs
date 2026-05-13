use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("omap_value", HashMap::from([("first", 1)])),
        ("sibling_lists", HashMap::from([("numbers", vec![1, 2]), ("strings", vec!["x", "y"])])),
        ("ref_marker_present", vec!["$keep", "z"]),
    ]);
    let _ = my_data;
}
