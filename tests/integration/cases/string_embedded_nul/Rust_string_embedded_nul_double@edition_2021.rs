use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("x", "\0"),
        ("y", "\01"),
    ]);
    let _ = my_data;
}
