use std::collections::HashMap;
fn main() {
    {
        let mut my_data = HashMap::from([
            ("name", "Alice"),
            ("scores", "[10, 20, 30]"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("name", "Alice"),
        ("scores", "[10, 20, 30]"),
    ]);
    let _ = my_data;
}
