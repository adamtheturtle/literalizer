use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        ("08", "value"),
    ]);
    let _ = &my_data;
}
