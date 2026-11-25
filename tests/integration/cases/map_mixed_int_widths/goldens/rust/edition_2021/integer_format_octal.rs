use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", 0o1),
        ("b", 0o20000000000000i64),
    ]);
    let _ = &my_data;
}
