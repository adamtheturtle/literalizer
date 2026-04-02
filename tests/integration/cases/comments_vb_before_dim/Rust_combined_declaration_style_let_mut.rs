use std::collections::HashMap;
fn main() {
    {
        let mut my_data = HashMap::from([
            // Configuration
            ("name", "app"),
            // Port setting
            ("port", "3000"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        // Configuration
        ("name", "app"),
        // Port setting
        ("port", "3000"),
    ]);
    let _ = my_data;
}
