use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", HashMap::from([("b", HashMap::from([("c", HashMap::from([("$ref", "deep")]))]))])),
    ]);
    let _ = my_data;
}
