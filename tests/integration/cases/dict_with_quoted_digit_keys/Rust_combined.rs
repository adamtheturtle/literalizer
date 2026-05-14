use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("0a", "first"),
        ("1b", "second"),
    ]);
    my_data = HashMap::from([
        ("0a", "first"),
        ("1b", "second"),
    ]);
    let _ = my_data;
}
