use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        ("name", "Alice"),
        ("scores", "[10, 20, 30]"),
    ]);
    let _ = my_data;
}
