use std::collections::HashSet;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashSet::from([
        // before apple
        "apple",
        "banana",  // banana inline
        // trailing
    ]);
    let _ = &my_data;
    my_data = HashSet::from([
        // before apple
        "apple",
        "banana",  // banana inline
        // trailing
    ]);
    let _ = &mut my_data;
}
