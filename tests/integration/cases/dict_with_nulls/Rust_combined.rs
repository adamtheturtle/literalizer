use std::collections::{HashMap};
fn main() {
    {
        let my_data = HashMap::from([
            ("name", "Alice"),
            ("score", "None"),
            ("age", "30"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("name", "Alice"),
        ("score", "None"),
        ("age", "30"),
    ]);
    let _ = my_data;
}
