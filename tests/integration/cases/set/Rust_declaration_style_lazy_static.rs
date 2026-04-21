use std::sync::LazyLock;
use std::collections::HashSet;
fn main() {
    static my_data: LazyLock<HashSet<&str>> = LazyLock::new(|| HashSet::from([
        "apple",
        "banana",
        "cherry",
    ]));
    let _ = my_data;
}
