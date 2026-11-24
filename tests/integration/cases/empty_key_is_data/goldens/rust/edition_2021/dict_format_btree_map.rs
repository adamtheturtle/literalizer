use std::collections::BTreeMap;
fn main() {
    let my_data = vec![
        BTreeMap::from([("", "external_value")]),
    ];
    let _ = &my_data;
}
