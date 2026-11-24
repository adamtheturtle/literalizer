use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("entries", vec![HashMap::from([("id", 1)])]),
    ]);
    let _ = &my_data;
}
