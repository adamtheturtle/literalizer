use std::collections::HashMap;
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
