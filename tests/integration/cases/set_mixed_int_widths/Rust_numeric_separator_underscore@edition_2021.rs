use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        1,
        1_099_511_627_776i64,
    ]);
    let _ = &my_data;
}
