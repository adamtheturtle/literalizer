use std::collections::BTreeMap;
fn main() {
    let my_data = vec![
        BTreeMap::from([("mapping", BTreeMap::<String, String>::from([]))]),
        <BTreeMap<&str, BTreeMap<String, String>>>::from([]),
    ];
    let _ = &my_data;
}
