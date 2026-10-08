use std::collections::HashMap;
fn main() {
    let existing = 1;
    let my_data = HashMap::from([
        ("nested", vec![0, existing]),
    ]);
    let _ = my_data;
}
