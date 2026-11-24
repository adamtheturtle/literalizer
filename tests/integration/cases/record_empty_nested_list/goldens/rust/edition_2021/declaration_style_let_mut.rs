use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("a", vec![vec![1, 2], vec![3]]),
        ("b", vec![Vec::new(), vec![1]]),
    ]);
    let _ = &mut my_data;
}
