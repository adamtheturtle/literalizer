use std::collections::{HashSet};
fn main() {
    let _ = HashSet::from([
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    ]);
}
