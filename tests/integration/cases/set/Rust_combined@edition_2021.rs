use std::collections::HashSet;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashSet::from([
        "apple",
        "banana",
        "cherry",
    ]);
    let _ = &my_data;
    my_data = HashSet::from([
        "apple",
        "banana",
        "cherry",
    ]);
    let _ = &mut my_data;
}
