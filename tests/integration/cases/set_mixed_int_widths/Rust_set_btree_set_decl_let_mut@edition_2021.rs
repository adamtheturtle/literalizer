use std::collections::BTreeSet;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = BTreeSet::from([
        1,
        1099511627776i64,
    ]);
    let _ = &mut my_data;
}
