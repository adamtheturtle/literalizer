use std::collections::BTreeMap;
fn main() {
    let mut my_data = BTreeMap::from([
        (1, "one"),
        (2, "two"),
        (42, "answer"),
    ]);
    let _ = my_data;
}
