use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("a", vec![1]),
        ("b", vec!["x"]),
    ]);
    my_data = HashMap::from([
        ("a", vec![1]),
        ("b", vec!["x"]),
    ]);
    let _ = my_data;
}
