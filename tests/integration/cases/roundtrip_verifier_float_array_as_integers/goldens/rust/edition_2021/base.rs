use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("value", vec![0, 1]),
    ]);
    let _ = &my_data;
}
