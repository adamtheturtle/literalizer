use std::collections::HashMap;
fn main() {
    let existing = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = existing;
    let _ = my_data;
}
