use std::collections::HashSet;
fn main() {
    {
        let mut my_data = HashSet::from([
            "apple",  // inline comment
            // before banana
            "banana",
            // trailing
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashSet::from([
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    ]);
    let _ = my_data;
}
