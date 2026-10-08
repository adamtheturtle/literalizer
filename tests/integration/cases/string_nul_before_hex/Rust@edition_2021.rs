use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("x", "before\0after"),
    ]);
    let _ = my_data;
}
