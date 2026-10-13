use std::collections::BTreeSet;
#[allow(non_snake_case)]
fn main() {
    let my_data = BTreeSet::from([
        "apple",
        "banana",
        "cherry",
    ]);
    let _ = &my_data;
}
