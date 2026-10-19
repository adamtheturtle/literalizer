use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        -2147483649i64,
        -2147483648,
        2147483647,
        2147483648i64,
        4085195400i64,
    ]);
    let _ = &my_data;
}
