use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    ]);
    let _ = my_data;
}
