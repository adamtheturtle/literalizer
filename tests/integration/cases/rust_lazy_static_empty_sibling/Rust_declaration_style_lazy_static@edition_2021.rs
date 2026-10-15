use std::sync::LazyLock;
use std::collections::HashMap;
fn main() {
    static MY_DATA: LazyLock<HashMap<&str, Vec<Vec<i32>>>> = LazyLock::new(|| HashMap::from([
        ("a", vec![vec![1, 2], vec![3]]),
        ("b", vec![Vec::new(), vec![1]]),
    ]));
    let _ = &MY_DATA;
}
