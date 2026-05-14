use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("metrics", HashMap::from([("count", 100), ("rate", 50)])),
        ("flags", HashMap::from([("retries", 3), ("timeout", 30)])),
    ]);
    let _ = my_data;
}
