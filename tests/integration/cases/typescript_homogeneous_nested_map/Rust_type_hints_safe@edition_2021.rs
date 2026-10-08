use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("first", HashMap::from([("x", 1), ("y", 2)])),
        ("second", HashMap::from([("z", 3)])),
    ]);
    let _ = my_data;
}
