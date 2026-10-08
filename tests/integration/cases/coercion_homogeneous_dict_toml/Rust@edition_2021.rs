use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("_", HashMap::from([("a", 1), ("b", 2)])),
    ]);
    let _ = my_data;
}
