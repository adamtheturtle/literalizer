use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("name", "Alice"),
        ("age", "30"),
        ("active", "True"),
    ]);
    my_data = HashMap::from([
        ("name", "Alice"),
        ("age", "30"),
        ("active", "True"),
    ]);
    let _ = my_data;
}
