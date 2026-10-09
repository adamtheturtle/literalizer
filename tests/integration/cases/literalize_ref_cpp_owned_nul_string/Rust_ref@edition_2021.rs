use std::collections::HashMap;
fn main() {
    let shared = "a\0b";
    let my_data = HashMap::from([
        ("value", shared),
    ]);
    let _ = my_data;
}
