use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", HashMap::from([("k", 2208988800)])),
        ("b", HashMap::from([("k", 1)])),
    ]);
    let _ = my_data;
}
