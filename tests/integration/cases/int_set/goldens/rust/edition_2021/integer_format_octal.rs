use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        0o1,
        0o2,
        0o3,
    ]);
    let _ = &my_data;
}
