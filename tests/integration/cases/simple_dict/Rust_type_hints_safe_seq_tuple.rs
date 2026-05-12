use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("name", "Alice"),
        ("age", 30),
        ("active", true),
        ("score", None::<()>),
    ]);
    let _ = my_data;
}
