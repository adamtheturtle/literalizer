use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("name", "Alice"),
        ("scores", "{\"1\": \"first\", \"2\": \"second\"}"),
    ]);
    my_data = HashMap::from([
        ("name", "Alice"),
        ("scores", "{\"1\": \"first\", \"2\": \"second\"}"),
    ]);
    let _ = my_data;
}
