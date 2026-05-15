use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("items", vec![HashMap::from([("id", 1)]), HashMap::from([("id", 2), ("count", 10)]), HashMap::from([("id", 3), ("count", 20)])]),
    ]);
    my_data = HashMap::from([
        ("items", vec![HashMap::from([("id", 1)]), HashMap::from([("id", 2), ("count", 10)]), HashMap::from([("id", 3), ("count", 20)])]),
    ]);
    let _ = my_data;
}
