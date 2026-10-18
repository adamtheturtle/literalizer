use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", vec![HashMap::from([("item", vec![1])])]),
        ("b", vec![HashMap::from([("item", vec![2])])]),
    ]);
    let _ = &my_data;
}
