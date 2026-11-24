use std::collections::HashSet;
fn main() {
    let mut my_data = HashSet::<String>::new();
    let _ = &my_data;
    my_data = HashSet::<String>::new();
    let _ = &mut my_data;
}
