use std::collections::HashSet;
fn main() {
    let mut my_data = vec![
        HashSet::from(["a", "b"]),
    ];
    let _ = &my_data;
    my_data = vec![
        HashSet::from(["a", "b"]),
    ];
    let _ = &mut my_data;
}
