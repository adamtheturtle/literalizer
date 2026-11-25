use std::sync::LazyLock;
use std::collections::HashSet;
fn main() {
    static MY_DATA: LazyLock<HashSet<i64>> = LazyLock::new(|| HashSet::from([
        1,
        1099511627776i64,
    ]));
    let _ = &MY_DATA;
}
