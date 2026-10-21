use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", 0b1),
        ("b", 0b10000000000000000000000000000000000000000i64),
    ]);
    let _ = &my_data;
}
