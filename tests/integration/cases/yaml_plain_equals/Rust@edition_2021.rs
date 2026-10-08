use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("x", "="),
        // unrelated
    ]);
    let _ = my_data;
}
