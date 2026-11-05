use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        ("section", BTreeMap::from([("value", 1)])),
    ]);
    let _ = &my_data;
}
