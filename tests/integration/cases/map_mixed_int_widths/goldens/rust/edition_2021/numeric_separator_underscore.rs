use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", 1),
        ("b", 1_099_511_627_776i64),
    ]);
    let _ = &my_data;
}
