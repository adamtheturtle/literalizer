use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", vec![1]),
        ("b", vec![1_099_511_627_776i64]),
    ]);
    let _ = &my_data;
}
