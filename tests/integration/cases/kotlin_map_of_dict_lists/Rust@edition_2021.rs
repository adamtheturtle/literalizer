use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", vec![HashMap::from([("k", 1)])]),
        ("b", vec![HashMap::from([("k", 2)])]),
    ]);
    let _ = my_data;
}
