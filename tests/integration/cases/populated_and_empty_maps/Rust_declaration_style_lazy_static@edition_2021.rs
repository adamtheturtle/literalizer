use std::sync::LazyLock;
use std::collections::HashMap;
fn main() {
    static my_data: LazyLock<Vec<HashMap<&str, i32>>> = LazyLock::new(|| vec![
        HashMap::from([("a", 1)]),
        <HashMap<&str, i32>>::from([]),
    ]);
    let _ = my_data;
}
