use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("a", "1"),
        ("b", "2.5"),
        ("c", "3"),
    ]);
    my_data = HashMap::from([
        ("a", "1"),
        ("b", "2.5"),
        ("c", "3"),
    ]);
    let _ = my_data;
}
