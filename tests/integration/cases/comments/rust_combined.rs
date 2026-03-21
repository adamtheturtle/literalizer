fn main() {
    {
        let my_data = HashMap::from(vec![
            // Server configuration
            ("host", "localhost"),  // default host
            ("port", "8080"),
            // Enable debug mode
            ("debug", "True"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from(vec![
        // Server configuration
        ("host", "localhost"),  // default host
        ("port", "8080"),
        // Enable debug mode
        ("debug", "True"),
    ]);
    let _ = my_data;
}
