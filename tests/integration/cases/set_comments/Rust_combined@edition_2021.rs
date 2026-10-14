use std::collections::HashSet;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashSet::from([
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    ]);
    let _ = &my_data;
    my_data = HashSet::from([
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    ]);
    let _ = &mut my_data;
}
