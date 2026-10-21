use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        0o1,
        0o20000000000000i64,
    ]);
    let _ = &my_data;
}
