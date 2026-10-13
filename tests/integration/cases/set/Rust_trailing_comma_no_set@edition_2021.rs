use std::collections::HashSet;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashSet::from([
        "apple",
        "banana",
        "cherry"
    ]);
    let _ = &my_data;
}
