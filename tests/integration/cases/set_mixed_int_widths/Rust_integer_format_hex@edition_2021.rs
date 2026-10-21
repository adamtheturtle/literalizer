use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        0x1,
        0x10000000000i64,
    ]);
    let _ = &my_data;
}
