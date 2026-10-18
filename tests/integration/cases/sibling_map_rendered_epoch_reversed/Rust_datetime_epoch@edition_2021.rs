use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("b", HashMap::from([("k", 1)])),
        ("a", HashMap::from([("k", 2208988800i64)])),
    ]);
    let _ = &my_data;
}
