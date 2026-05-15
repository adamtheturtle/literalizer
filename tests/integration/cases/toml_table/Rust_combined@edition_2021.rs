use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("section", HashMap::from([("value", 1)])),
    ]);
    my_data = HashMap::from([
        ("section", HashMap::from([("value", 1)])),
    ]);
    let _ = my_data;
}
