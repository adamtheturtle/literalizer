use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        // outer heading
        // first empty
        ("a", HashMap::<String, String>::from([])),
        // second empty
        ("b", HashMap::<String, String>::from([])),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        // outer heading
        // first empty
        ("a", HashMap::<String, String>::from([])),
        // second empty
        ("b", HashMap::<String, String>::from([])),
    ]);
    let _ = &mut my_data;
}
