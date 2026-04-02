use std::collections::HashSet;
fn main() {
    {
        let mut my_data = HashSet::from([
            // before apple
            "apple",
            "banana",  // banana inline
            // trailing
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashSet::from([
        // before apple
        "apple",
        "banana",  // banana inline
        // trailing
    ]);
    let _ = my_data;
}
