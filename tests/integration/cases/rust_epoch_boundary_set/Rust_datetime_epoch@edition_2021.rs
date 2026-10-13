use std::collections::HashSet;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashSet::from([
        -2147483649i64,
        -2147483648,
        2147483647,
        2147483648i64,
    ]);
    let _ = &my_data;
}
