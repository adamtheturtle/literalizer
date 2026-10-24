use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        ("a\"b", 1),
    ]);
    let _ = &my_data;
}
