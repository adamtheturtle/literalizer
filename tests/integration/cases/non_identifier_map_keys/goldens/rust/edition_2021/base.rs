use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a-b", 1),
        ("two words", 2),
        ("she said \"hi\"", 3),
        ("", 4),
        ("valid_key", 5),
    ]);
    let _ = &my_data;
}
