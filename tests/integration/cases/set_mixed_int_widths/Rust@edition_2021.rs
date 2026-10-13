use std::collections::HashSet;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashSet::from([
        1,
        1099511627776i64,
    ]);
    let _ = &my_data;
}
