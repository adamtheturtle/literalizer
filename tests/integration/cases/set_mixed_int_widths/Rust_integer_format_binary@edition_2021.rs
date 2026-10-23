use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        0b1,
        0b10000000000000000000000000000000000000000i64,
    ]);
    let _ = &my_data;
}
