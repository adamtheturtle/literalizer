use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", vec![vec![1], vec![2]]),
        ("b", vec![vec!["x"], vec!["y"]]),
    ]);
    let _ = my_data;
}
