use std::collections::BTreeMap;
fn main() {
    let my_data = vec![
        BTreeMap::from([("scores", vec![1, 2])]),
        BTreeMap::from([("scores", vec![3, 4])]),
    ];
    let _ = my_data;
}
