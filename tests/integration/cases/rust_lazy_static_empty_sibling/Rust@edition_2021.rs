use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", vec![vec![1, 2], vec![3]]),
        ("b", vec![vec![], vec![1]]),
    ]);
    let _ = my_data;
}
