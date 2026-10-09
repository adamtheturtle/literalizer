use std::collections::HashMap;
fn main() {
    let shared = "s";
    let my_data = HashMap::from([
        ("value", shared),
    ]);
    let _ = my_data;
}
