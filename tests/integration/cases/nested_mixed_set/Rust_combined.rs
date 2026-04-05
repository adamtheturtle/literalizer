use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    let mut my_data = HashMap::from([
        ("name", "Alice"),
        ("tags", "[\"42\", \"True\", \"apple\"]"),
    ]);
    my_data = HashMap::from([
        ("name", "Alice"),
        ("tags", "[\"42\", \"True\", \"apple\"]"),
    ]);
    let _ = my_data;
}
