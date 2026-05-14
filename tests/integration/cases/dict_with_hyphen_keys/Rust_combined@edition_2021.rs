use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("my-key", "value1"),
        ("another-key", "value2"),
        ("normal_key", "value3"),
    ]);
    my_data = HashMap::from([
        ("my-key", "value1"),
        ("another-key", "value2"),
        ("normal_key", "value3"),
    ]);
    let _ = my_data;
}
