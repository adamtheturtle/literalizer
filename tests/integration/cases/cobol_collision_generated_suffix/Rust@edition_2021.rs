use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a-b", 1),
        ("a b", 2),
        ("a-b-2", 3),
    ]);
    let _ = my_data;
}
