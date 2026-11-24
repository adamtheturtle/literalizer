use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("first", HashMap::from([("x", 1)])),
        ("second", HashMap::from([("y", 2)])),
    ]);
    let _ = &my_data;
}
