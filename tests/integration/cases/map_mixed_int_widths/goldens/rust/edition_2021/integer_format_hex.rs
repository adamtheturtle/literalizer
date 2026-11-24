use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", 0x1),
        ("b", 0x10000000000i64),
    ]);
    let _ = &my_data;
}
