use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    {
        let my_data = HashMap::from([
            // Server configuration
            ("host", "localhost"),  // default host
            ("port", 8080),
            // Enable debug mode
            ("debug", true),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        // Server configuration
        ("host", "localhost"),  // default host
        ("port", 8080),
        // Enable debug mode
        ("debug", true),
    ]);
    let _ = my_data;
}
