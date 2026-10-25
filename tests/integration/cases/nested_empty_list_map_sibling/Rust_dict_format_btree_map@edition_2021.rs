use std::collections::BTreeMap;
fn main() {
    let my_data = vec![
        BTreeMap::from([("values", Vec::<String>::new())]),
        <BTreeMap<&str, Vec<String>>>::from([]),
    ];
    let _ = &my_data;
}
