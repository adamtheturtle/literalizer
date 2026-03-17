use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    {
        let my_data = HashMap::from([
            ("name", "Alice"),
            ("score", None),
            ("age", 30),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("name", "Alice"),
        ("score", None),
        ("age", 30),
    ]);
    let _ = my_data;
}
