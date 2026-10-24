use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        ("a", vec![1]),
        ("b", Vec::new()),
    ]);
    let _ = &my_data;
}
