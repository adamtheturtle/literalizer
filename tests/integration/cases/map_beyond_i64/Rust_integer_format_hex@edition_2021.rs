use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", 0x7fffffffffffffffi128),
        ("b", 0x8000000000000000i128),
    ]);
    let _ = &my_data;
}
