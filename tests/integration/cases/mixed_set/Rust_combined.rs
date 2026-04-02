use std::collections::HashSet;
fn main() {
    let mut my_data = HashSet::from([
        "42",
        "True",
        "apple",
    ]);
    my_data = HashSet::from([
        "42",
        "True",
        "apple",
    ]);
    let _ = my_data;
}
