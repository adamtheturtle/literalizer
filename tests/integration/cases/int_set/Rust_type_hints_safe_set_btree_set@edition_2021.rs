use std::collections::BTreeSet;
#[allow(non_snake_case)]
fn main() {
    let my_data = BTreeSet::from([
        1,
        2,
        3,
    ]);
    let _ = &my_data;
}
