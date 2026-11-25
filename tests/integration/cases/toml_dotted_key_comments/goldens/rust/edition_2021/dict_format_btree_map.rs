use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        // first dotted key
        // second dotted key
        ("a", BTreeMap::from([("b", 1), ("c", 2)])),
    ]);
    let _ = &my_data;
}
