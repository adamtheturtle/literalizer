use std::collections::HashMap;
fn main() {
    {
        let mut my_data = HashMap::from([
            ("name", "Alice"),
            ("age", "30"),
            ("active", "True"),
            ("score", "None"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("name", "Alice"),
        ("age", "30"),
        ("active", "True"),
        ("score", "None"),
    ]);
    let _ = my_data;
}
