use std::collections::HashSet;
fn main() {
    let mut my_data = HashSet::from([
        "apple",
        "banana",
        "cherry",
    ]);
    let _ = &mut my_data;
}
