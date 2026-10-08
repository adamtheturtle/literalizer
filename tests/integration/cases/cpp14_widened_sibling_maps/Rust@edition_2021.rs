use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", HashMap::from([("k", 1)])),
        ("b", HashMap::from([("k", "s")])),
    ]);
    let _ = my_data;
}
