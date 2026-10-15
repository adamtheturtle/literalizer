use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        // outer heading
        // first empty
        ("a", HashMap::<String, String>::from([])),
        // second empty
        ("b", HashMap::<String, String>::from([])),
    ]);
    let _ = &my_data;
}
