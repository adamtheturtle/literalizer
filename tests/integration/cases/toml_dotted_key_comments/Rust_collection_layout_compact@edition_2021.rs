use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        // first dotted key
        // second dotted key
        ("a", HashMap::from([("b", 1), ("c", 2)])),
    ]);
    let _ = &my_data;
}
