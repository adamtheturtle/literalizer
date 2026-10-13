use std::collections::HashSet;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashSet::from([
        1,
        1099511627776i64,
    ]);
    let _ = &my_data;
    my_data = HashSet::from([
        1,
        1099511627776i64,
    ]);
    let _ = &mut my_data;
}
