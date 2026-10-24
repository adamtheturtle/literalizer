use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("_", [1, 2, 3]),
    ]);
    let _ = &my_data;
}
