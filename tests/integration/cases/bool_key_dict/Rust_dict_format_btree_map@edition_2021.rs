use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        (true, "yes"),
        (false, "no"),
    ]);
    let _ = &my_data;
}
