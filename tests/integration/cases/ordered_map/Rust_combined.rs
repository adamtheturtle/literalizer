use std::collections::{HashMap};
fn main() {
    {
        let my_data = HashMap::from([
            ("name", "Alice"),
            ("age", "30"),
            ("active", "True"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("name", "Alice"),
        ("age", "30"),
        ("active", "True"),
    ]);
    let _ = my_data;
}
