use std::collections::BTreeMap;
fn main() {
    let my_data = vec![
        BTreeMap::from([("a", vec![1])]),
        BTreeMap::from([("a", vec![2])]),
    ];
    let _ = my_data;
}
