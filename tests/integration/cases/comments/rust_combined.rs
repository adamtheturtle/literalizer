use std::collections::{HashMap};
fn main() {
    {
        let my_data = HashMap::from([
            // Server configuration
            ("host", "localhost"),  // default host
            ("port", "8080"),
            // Enable debug mode
            ("debug", "True"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        // Server configuration
        ("host", "localhost"),  // default host
        ("port", "8080"),
        // Enable debug mode
        ("debug", "True"),
    ]);
    let _ = my_data;
}
