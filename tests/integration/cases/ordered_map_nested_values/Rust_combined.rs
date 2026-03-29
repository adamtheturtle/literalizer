use std::collections::HashMap;
fn main() {
    {
        let my_data = HashMap::from([
            ("name", "Alice"),
            ("scores", "{\"1\": \"first\", \"2\": \"second\"}"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("name", "Alice"),
        ("scores", "{\"1\": \"first\", \"2\": \"second\"}"),
    ]);
    let _ = my_data;
}
