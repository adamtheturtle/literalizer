use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", HashMap::from([("k", "07:30:00")])),
        ("b", HashMap::from([("k", "string")])),
    ]);
    let _ = &my_data;
}
