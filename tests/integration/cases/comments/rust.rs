use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    let _ = HashMap::from([
        // Server configuration
        ("host", "localhost"), // default host
        ("port", 8080),
        // Enable debug mode
        ("debug", true),
    ]);
}
