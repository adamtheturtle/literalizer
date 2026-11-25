use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        0b1,
        0b10,
        0b11,
    ]);
    let _ = &my_data;
}
