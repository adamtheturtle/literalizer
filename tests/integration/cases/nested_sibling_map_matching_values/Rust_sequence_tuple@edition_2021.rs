use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("first", HashMap::from([("items", (1, HashMap::from([("value", 2)])))])),
        ("second", HashMap::from([("items", (1, HashMap::from([("value", 3)])))])),
    ]);
    let _ = &my_data;
}
