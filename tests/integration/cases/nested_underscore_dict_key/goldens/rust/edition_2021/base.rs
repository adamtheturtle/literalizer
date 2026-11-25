use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("outer", vec![HashMap::from([("_", 1)])]),
    ]);
    let _ = &my_data;
}
