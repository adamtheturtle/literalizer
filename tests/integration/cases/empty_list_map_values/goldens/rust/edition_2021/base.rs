use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", vec![1]),
        ("b", Vec::new()),
    ]);
    let _ = &my_data;
}
