use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        ("a", vec![BTreeMap::from([("item", vec![1])])]),
        ("b", vec![BTreeMap::from([("item", vec![2, 3])])]),
    ]);
    let _ = &my_data;
}
