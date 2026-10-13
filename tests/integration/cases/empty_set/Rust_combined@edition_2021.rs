use std::collections::HashSet;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashSet::<String>::new();
    let _ = &my_data;
    my_data = HashSet::<String>::new();
    let _ = &mut my_data;
}
