use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("a", "{\"x\": 1}"),
        ("b", "2"),
    ]);
    my_data = HashMap::from([
        ("a", "{\"x\": 1}"),
        ("b", "2"),
    ]);
    let _ = my_data;
}
